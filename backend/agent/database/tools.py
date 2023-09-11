"""Toolkit for interacting with a SQL database."""

from backend.agent.database.sql_tool import CustomSQL
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
from langchain.tools import BaseTool
from langchain.agents.agent_toolkits.base import BaseToolkit
from langchain.schema.language_model import BaseLanguageModel
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from typing import Optional, Any
from pydantic import BaseModel, Extra, Field, root_validator
from langchain.tools.sql_database.prompt import QUERY_CHECKER
from typing import Any, Dict, Optional, List, Type
import re


def extract_values(input_string: str):
    pattern = r'(\w+):\s*(\[?\w+-?\w*\]?)'
    matches = re.findall(pattern, input_string)
    result = {key: value.strip('[]') for key, value in matches}

    return result


class CustomBaseSQLDatabaseTool(BaseModel):
    """Base tool for interacting with a SQL database."""

    db: CustomSQL = Field(exclude=True)

    # Override BaseTool.Config to appease mypy
    # See https://github.com/pydantic/pydantic/issues/4173
    class Config(BaseTool.Config):
        """Configuration for this pydantic object."""

        arbitrary_types_allowed = True
        extra = Extra.forbid


class CustomGetAllTablesTool(CustomBaseSQLDatabaseTool, BaseTool):
    name = "list_sql_tables_tool"
    description = """
        This tool is useful when you need to get all tables from a database.
    """

    def _run(self, tool_input: str = "", run_manager: Optional[CallbackManagerForToolRun] = None):
        """Get the schema for a specific table."""

        return self.db._all_tables

    async def _arun(
        self,
        tool_input: str = "",
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        raise NotImplementedError(
            "sql_db_get_all_tables does not support async")


class CustomListSQLDatabaseTool(CustomBaseSQLDatabaseTool, BaseTool):
    """Tool for getting tables names."""

    name = "sql_db_list_tables"
    description = """
        Use this tool when you already know what are the tables ONLY!
        Otherwise please use: list_sql_tables_tool first!
    """

    def _run(
        self,
        tool_input: str = "",
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Get the schema for a specific table."""
        return ", ".join(self.db.get_usable_table_names())

    async def _arun(
        self,
        tool_input: str = "",
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        return ", ".join(self.db.get_usable_table_names())


class CustomQuerySQLDataBaseTool(CustomBaseSQLDatabaseTool, BaseTool):
    """Tool for querying a SQL database."""

    name = "sql_db_query"
    description = """
    Input to this tool is a detailed and correct SQL query, output is a result from the database.
    If the query is not correct, an error message will be returned.
    If an error is returned, rewrite the query, check the query, and try again.
    """

    def _run(
        self,
        query: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Execute the query, return the results or an error message."""
        return self.db.run_no_throw(query)

    async def _arun(
        self,
        query: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        """Execute the query, return the results or an error message."""
        return self.db.run_no_throw(query)


class CustomInfoSQLDatabaseTool(CustomBaseSQLDatabaseTool, BaseTool):
    """Tool for getting metadata about a SQL database."""

    name = "sql_db_schema"
    description = """
    Input to this tool is a comma-separated list of tables, output is the schema and sample rows for those tables.    
    Example Input: "table1, table2, table3", But If you don't know a table DONT USE THIS TOOL.
    """

    def _run(
        self,
        table_names: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Get the schema for tables in a comma-separated list."""
        return self.db.get_table_info_no_throw(table_names.split(", "))

    async def _arun(
        self,
        table_names: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        """Get the schema for tables in a comma-separated list."""
        return self.db.get_table_info_no_throw(table_names.split(", "))


class QuerySQLCheckerTool(CustomBaseSQLDatabaseTool, BaseTool):
    """Use an LLM to check if a query is correct.
    Adapted from https://www.patterns.app/blog/2023/01/18/crunchbot-sql-analyst-gpt/"""

    template: str = QUERY_CHECKER
    llm: BaseLanguageModel
    llm_chain: LLMChain = Field(init=False)
    name = "sql_db_query_checker"
    description = """
    Use this tool to double check if your query is correct before executing it.
    Always use this tool before executing a query with query_sql_db!
    """

    @root_validator(pre=True)
    def initialize_llm_chain(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        if "llm_chain" not in values:
            values["llm_chain"] = LLMChain(
                llm=values.get("llm"),
                prompt=PromptTemplate(
                    template=QUERY_CHECKER, input_variables=[
                        "query", "dialect"]
                ),
            )

        if values["llm_chain"].prompt.input_variables != ["query", "dialect"]:
            raise ValueError(
                "LLM chain for QueryCheckerTool must have input variables ['query', 'dialect']"
            )

        return values

    def _run(
        self,
        query: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Use the LLM to check the query."""
        return self.llm_chain.predict(query=query, dialect=self.db.dialect)

    async def _arun(
        self,
        query: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        return await self.llm_chain.apredict(query=query, dialect=self.db.dialect)


class CustomSQLDatabaseToolkit(BaseToolkit):
    """Toolkit for interacting with SQL databases."""

    db: CustomSQL = Field(exclude=True)
    llm: BaseLanguageModel = Field(exclude=True)

    class Config:
        """Configuration for this pydantic object."""

        arbitrary_types_allowed = True

    @property
    def dialect(self) -> str:
        """Return string representation of dialect to use."""
        return self.db.dialect

    def get_tools(self) -> List[BaseTool]:
        """Get the tools in the toolkit."""
        list_sql_tables_tool = CustomGetAllTablesTool(db=self.db)
        list_sql_tables_tool.description = (
            "In order to get all tables, you need to write SQL command to get all tables"
        )

        list_sql_database_tool = CustomListSQLDatabaseTool(db=self.db)
        info_sql_database_tool_description = (
            "Input to this tool is a comma-separated list of tables, output is the "
            "schema and sample rows for those tables. "
            "Be sure that the tables actually exist by calling"
            f"{list_sql_tables_tool.name} first! "
            f"Dont use example input as input use values from {list_sql_tables_tool.name} instead"
            "Example Input: 'table1, table2, table3'"
        )

        info_sql_database_tool = CustomInfoSQLDatabaseTool(
            db=self.db, description=info_sql_database_tool_description
        )
        query_sql_database_tool_description = (
            "Input to this tool is a detailed and correct SQL query, output is a "
            "result from the database. If the query is not correct, an error message "
            "will be returned. If an error is returned, rewrite the query, check the "
            "query, and try again. If you encounter an issue with Unknown column "
            f"'xxxx' in 'field list', using {info_sql_database_tool.name} "
            "to query the correct table fields."
        )
        query_sql_database_tool = CustomQuerySQLDataBaseTool(
            db=self.db, description=query_sql_database_tool_description
        )

        query_sql_checker_tool_description = (
            "Use this tool to double check if your query is correct before executing "
            "it. Always use this tool before executing a query with "
            f"{query_sql_database_tool.name}!"
        )
        query_sql_checker_tool = QuerySQLCheckerTool(
            db=self.db, llm=self.llm, description=query_sql_checker_tool_description
        )

        return [
            query_sql_database_tool,
            info_sql_database_tool,
            list_sql_database_tool,
            query_sql_checker_tool,
        ]
