from sqlalchemy.orm import Session
from core.config import settings
import os

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

from core.prompts import STORY_PROMPT
from models.story import Story, StoryNode
from core.models import StoryLLMResponse, StoryNodeLLM
# from dotenv import load_dotenv

# load_dotenv()


class StoryGenerator:
    @classmethod
    def _get_llm(cls):
        openai_api_key = os.getenv("CHOREO_OPENAI_CONNECTION_OPENAI_API_KEY")
        serviceurl = os.getenv("CHOREO_OPENAI_CONNECTION_SERVICEURL")

        if openai_api_key and serviceurl:
            return ChatOpenAI(model="04-mini", api_key=openai_api_key, base_url=serviceurl)
        
        return ChatOpenAI(model="o4-mini", api_key=settings.OPEN_API_KEY)

    @classmethod
    def generate_story(
        cls, db: Session, session_id: str, theme: str = "fantasy"
    ) -> Story:
        llm = cls._get_llm()
        story_parser = PydanticOutputParser(pydantic_object=StoryLLMResponse)

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", STORY_PROMPT),
                ("human", f"Create the story with this theme: {theme}"),
            ]
        ).partial(format_instructions=story_parser.get_format_instructions())

        raw_response = llm.invoke(
            prompt.invoke({})
        )  # first parse the prompt with invoke then invoke the prompt in the llm itself

        response_text = raw_response
        if hasattr(raw_response, "content"):
            response_text = raw_response.content

        story_structure = story_parser.parse(
            response_text
        )  # parse the response into the story object we want to use.

        story_db = Story(title=story_structure.title, session_id=session_id)
        db.add(story_db)  # add the Story obj to the db
        db.flush()  # This fills out all the db fields (like primary key etc.) for the added Story obj

        root_node_data = story_structure.rootNode

        if isinstance(root_node_data, dict):
            # this returns a StoryNode obj after vaildation.
            root_node_data = StoryNodeLLM.model_validate(
                root_node_data
            )  # make sure it has content, isending bool etc. from data model
            # auto raises error

        cls._process_story_node(
            node_data=root_node_data, db=db, story_id=story_db.id, is_root=True
        )

        db.commit()
        return story_db

    @classmethod
    def _process_story_node(
        cls, node_data: StoryNodeLLM, db: Session, story_id: int, is_root: bool = False
    ) -> StoryNode:
        # loop through nodedata to get the content, is_ending/winnig_ending, and optionn
        # find the next node in the options dict, do loop again.

        node = StoryNode(
            story_id=story_id,
            content=node_data.content
            if hasattr(node_data, "content")
            else node_data["content"],
            is_root=is_root,
            is_ending=node_data.isEnding
            if hasattr(node_data, "isEnding")
            else node_data["isEnding"],
            is_winning_ending=node_data.isWinningEnding
            if hasattr(node_data, "isWinningEnding")
            else node_data["isWinningEnding"],
            options=[],
        )

        db.add(node)
        db.flush()

        # if the node is not ending, has an options attr and that attr is not empty
        if not node.is_ending and (hasattr(node_data, "options") and node_data.options):
            options_list = []
            for option_data in node_data.options:
                next_node = option_data.nextNode

                if isinstance(next_node, dict):
                    next_node = StoryNodeLLM.model_validate(next_node)

                child_node = cls._process_story_node(
                    node_data=next_node, db=db, story_id=story_id, is_root=False
                )

                # Storing the data this way makes it so you don't have to store all the nodes in the options list
                # but can instead lookup the node as it's needed using it's ID from the DB.
                options_list.append(
                    {"text": option_data.text, "node_id": child_node.id}
                )

            node.options = options_list

        db.flush()
        return node
