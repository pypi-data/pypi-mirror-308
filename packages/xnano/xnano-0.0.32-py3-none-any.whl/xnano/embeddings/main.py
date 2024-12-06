# memory client
# qdrant vector store

from pathlib import Path
import uuid
from typing import Optional, Union, Dict, Any, List

from .._lib import console, XNANOException
from ..types.nlp.embeddings import EmbeddingModel
from ..types.documents.document import Document
from ..types.memories.memory import MemoryLocation, DistanceType, DataType

import httpx
from ..types.openai import ChatCompletionModality, ChatCompletionPredictionContentParam, ChatCompletionAudioParam
from ..types.completions.context import Context
from ..types.completions.chat_models import ChatModel
from ..types.completions.instructor import InstructorMode
from ..types.completions.messages import MessageType
from ..types.completions.responses import Response
from ..types.completions.response_models import ResponseModelType
from ..types.completions.tools import ToolChoice, ToolType


class Embeddings:

    def __init__(
        self,

        # qdrant client/store args
        collection_name : str = "xnano_collection",
        location : Union[MemoryLocation, Path] = ":memory:",
        distance : DistanceType = "cosine",
        dimensions : int = 1536,

        # hnsw
        hnsw : bool = False,
        hnsw_m : int = 48,

        # verbosity
        verbose : bool = False,
    ):
        
        """
        Initializes the Qdrant Vector Store

        Example:
        embeddings = Embeddings(
            collection_name = "my_collection",
            location = "./my_collection"
        )

        Args:
            collection_name (str): The name of the collection to use.
            location (Union[MemoryLocation, Path]): The location of the vector store.
            distance (DistanceType): The distance metric to use.
            dimensions (int): The number of dimensions to use.
            hnsw (bool): Whether to use HNSW.
            hnsw_m (int): The number of links to use.
            verbose (bool): Whether to print verbose messages.
        """

        # set verbosity
        self.verbose = verbose
        
        # set params
        self.collection_name = collection_name
        self.location = location
        self.distance = distance
        self.dimensions = dimensions
        # hnsw params
        self.hnsw = hnsw
        self.hnsw_m = hnsw_m

        # get imports
        from qdrant_client import QdrantClient

        try:
            if self._ensure_location_is_valid():
                self.client = QdrantClient(location=self.location)
            else:
                self.client = QdrantClient(path=self.location)
        except Exception as e:
            raise XNANOException(f"Invalid location: {e}") from e
        
        # init collection
        try:
            self._set_distance()
            self._create_or_load_collection()
        except Exception as e:
            raise XNANOException(f"Failed to initialize collection: {e}") from e
            

    def _ensure_location_is_valid(self) -> bool:
        """
        Ensures the location is valid & returns True if on memory
        """

        # if the location is not on memory, ensure we have a valid path
        if self.location != ":memory:":
            # Check if the location is a normal string and not a full path
            if not Path(self.location).is_absolute() and not self.location.startswith("./"):
                self.location = f"./{self.location}"

            path = Path(self.location)
            if path.exists() and path.is_dir():
                if self.verbose:
                    console.message(f"Loading Vector Store from Location: [sky_blue3]{self.location}[/sky_blue3]")
                return False
            
            if not path.exists() or not path.is_dir():
                path.mkdir(parents=True, exist_ok=True)  # Create the directory if it does not exist
                if self.verbose:
                    console.message(f"Created Vector Store at Location: [sky_blue3]{self.location}[/sky_blue3]")

            return False
        
        if self.verbose:
            console.message(f"Using [green]On Memory[/green] Vector Store")

        return True


    def _set_distance(self):
        """
        Sets the distance
        """
        try:
            from qdrant_client.models import Distance

            self.distance = Distance(self.distance.capitalize())

            if self.verbose:
                console.message(f"Using [sky_blue3]{self.distance}[/sky_blue3] Distance")
                console.message(f"Using a Dimension Size of [sky_blue3]{self.dimensions}[/sky_blue3]")

        except Exception as e:
            raise XNANOException(f"Invalid distance: {e}") from e


    def _create_or_load_collection(self):
        """
        Creates or loads the specified collection
        """
        from qdrant_client.models import VectorParams, HnswConfig

        if not self.client.collection_exists(self.collection_name):

            if self.verbose:
                console.message(f"Creating collection: [italic sky_blue3]{self.collection_name}[/italic sky_blue3]")

            if self.hnsw:
                if self.verbose:
                    console.message(f"Using [bold green]HNSW[/bold green] with [sky_blue3]{self.hnsw_m}[/sky_blue3] Links")
            
            try:
                self.client.create_collection(
                    collection_name = self.collection_name,
                    vectors_config = VectorParams(
                        size = self.dimensions,
                        distance = self.distance,
                        on_disk = False if self.location == ":memory:" else True
                    ),
                    hnsw_config = HnswConfig(
                        m = self.hnsw_m
                    ) if self.hnsw else None
                )
            except Exception as e:
                raise XNANOException(f"Failed to create collection: {e}") from e


    def _get_content_from_data(self, data: DataType, metadata: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Gets the content from the data & returns a list of dicts in 
        text, metadata format
        """
        import time
        import uuid

        if not isinstance(data, list):
            data = [data]

        if self.verbose:
            console.message(f"Adding [sky_blue3]{len(data)}[/sky_blue3] items to memory")

        content = []

        for item in data:
            item_metadata = {
                "time_added": time.time(),
                "id": str(uuid.uuid4()),
                "chunk_id": None,
                "embedding": None
            }

            if isinstance(item, str):
                content.append({
                    "text": item,
                    "metadata": {**item_metadata, **(metadata or {})},
                })

            elif isinstance(item, Document):
                if not item.metadata:
                    item_metadata["metadata"] = item_metadata
                else:
                    item_metadata = {**item_metadata, **item.metadata}

                content.append({
                    "text": item.text,
                    "metadata": item_metadata,
                })

            elif isinstance(item, Dict):
                content.append({
                    "text": item.get("text", ""),
                    "metadata": {**item_metadata, **(item.get("metadata", {}) or {})}
                })

            else:
                raise XNANOException(f"Invalid data type: {type(item)}")

        return content
    

    def _get_chunks(self, content : List[Dict[str, Any]], chunk_size : int = 2000) -> List[Dict[str, Any]]:
        """
        Gets the chunks from the content
        """
        import uuid
        from ..nlp import chunk
        
        results = []

        for item in content:

            if len(item["text"]) > chunk_size:

                try:

                    # TODO: 
                    # implement more sophisticated chunking
                    chunks = chunk(
                        inputs = item["text"],
                        chunk_size = chunk_size,
                        progress_bar = False
                    )

                    # Replace the item with the chunked documents
                    content = [
                        {
                            "text": chunk,
                            "metadata": {**item["metadata"].copy(), "chunk_id": str(uuid.uuid4())}
                        }
                        for chunk in chunks
                    ]

                    results.extend(content)

                    if self.verbose:
                            console.message(f"Chunked document [sky_blue3]{item['metadata']['id']}[/sky_blue3] into [sky_blue3]{len(chunks)}[/sky_blue3] chunks")

                except Exception as e:
                    raise XNANOException(f"Failed to chunk content for document {item['metadata']['id']}: {e}") from e
                
            else:
                results.append(item)

        return results


    def _get_embeddings(
        self,
        content: List[Dict[str, Any]],
        model: Union[str, EmbeddingModel],
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        organization: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Generates embeddings for the given content.
        If the content has chunk_id and chunks, it processes them accordingly.
        """
        embeddings = []
        from ..nlp.embedder import embedding

        for item in content:
            if "chunk_id" in item and "text" in item:
                # Process chunked content
                embedding_result = embedding(
                    item["text"], model=model,
                    dimensions=self.dimensions,
                    base_url=base_url,
                    api_key=api_key,
                    organization=organization
                )
                embeddings.append({
                    "chunk_id": item["chunk_id"],
                    "text": item["text"], 
                    "embedding": embedding_result if isinstance(embedding_result, list) else embedding_result['embedding'],
                    "metadata": item.get("metadata", {})
                })
            else:
                # Process non-chunked content
                embedding_result = embedding(
                    item["text"], model=model,
                    dimensions=self.dimensions,
                    base_url=base_url,
                    api_key=api_key,
                    organization=organization
                )

                if len(embedding_result) != self.dimensions:
                    raise XNANOException(f"Embedding dimensions mismatch: expected [bold]{self.dimensions}[/bold], got [bold]{len(embedding_result)}[/bold]. Try using a different model.")

                embeddings.append({
                    "text": item["text"],  # Preserve the text
                    "embedding": embedding_result if isinstance(embedding_result, list) else embedding_result['embedding'],
                    "metadata": item.get("metadata", {})
                })

        return embeddings
    

    def remove(
            self,
            ids: List[str]
    ):
        """
        Removes points from the collection

        Example:
        embeddings.remove(
            ids = ["123e4567-e89b-12d3-a456-426614174000", "123e4567-e89b-12d3-a456-426614174001"]
        )

        Args:
            ids (List[str]): The ids of the points to remove.
        """
        from qdrant_client.models import PointsSelector, Filter
        from qdrant_client.http.models.models import FilterSelector

        if self.verbose:
            console.message(f"Removing [sky_blue3]{len(ids)}[/sky_blue3] points from collection")

        try:
            for id in ids:
                self.client.delete(
                    collection_name=self.collection_name,
                    points_selector=PointsSelector(
                        filter=Filter(key="id", match=FilterSelector(value=id))
                    )
                )
        except Exception as e:
            raise XNANOException(f"Failed to remove points from collection: {e}") from e
        

    def save(
            self,
            location: Union[MemoryLocation, Path]
    ):
        if location == ":memory:":
            raise XNANOException("Cannot save to memory location. Please provide a valid file path or memory location.")

        try:
            self.client.save_collection(
                collection_name=self.collection_name,
                location=location
            )
        except Exception as e:
            raise XNANOException(f"Failed to save collection to {location}: {e}") from e


    def add(
        self,
        data: DataType,
        metadata: Optional[Dict[str, Any]] = None,
        chunk_size: int = 2000,
        model: Union[str, EmbeddingModel] = "text-embedding-3-small",
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        organization: Optional[str] = None,
    ):
        """
        Adds data to the memory

        Example:
        embeddings.add(
            data = ["Hello, world!", "This is a test"]
        )

        Args:
            data (DataType): The data to add.
            metadata (Optional[Dict[str, Any]]): The metadata to add.
            chunk_size (int): The chunk size to use.
            model (Union[str, EmbeddingModel]): The model to use.
            base_url (Optional[str]): The base URL to use.
            api_key (Optional[str]): The API key to use.
            organization (Optional[str]): The organization to use.
        """
        from qdrant_client.models import UpdateStatus, PointStruct

        # Get content
        try:
            content = self._get_content_from_data(data, metadata)
        except Exception as e:
            raise XNANOException(f"Failed to get content from data: {e}") from e

        # Create chunks if needed
        try:
            content = self._get_chunks(content, chunk_size)
        except Exception as e:
            raise XNANOException(f"Failed to get chunks from content: {e}") from e

        # Get embeddings
        try:
            content = self._get_embeddings(content, model, base_url, api_key, organization)
        except Exception as e:
            raise XNANOException(f"Failed to get embeddings from content: {e}") from e

        # Create points and handle missing 'embedding' key
        try:
            points = []
            for item in content:
                if "embedding" not in item:
                    raise XNANOException(f"Missing embedding in content item with metadata: {item.get('metadata', 'No metadata')}")
                
                # Create payload with metadata only (text is handled separately)
                payload = item["metadata"].copy()
                if "text" in payload:  # Remove text from metadata if it exists
                    del payload["text"]
                
                points.append(
                    PointStruct(
                        id=item["metadata"].get("id", str(uuid.uuid4())),
                        vector=item["embedding"],
                        payload={
                            **payload,
                            "text": item["text"]  # Add text at the top level
                        }
                    )
                )

        except Exception as e:
            raise XNANOException(f"Failed to create points & payloads: {e}") from e

        # Add to collection
        try:
            result = self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )
            if result.status == UpdateStatus.COMPLETED:
                if self.verbose:
                    console.message(f"Successfully added {len(points)} points to collection")
            else:
                raise XNANOException(f"Failed to add points to collection: {result.status}")
        except Exception as e:
            raise XNANOException(f"Failed to add points to collection: {e}") from e

        
    def search(
            self,
            query : Union[str, List[str]],
            model : Union[str, EmbeddingModel] = "text-embedding-3-small",
            base_url : Optional[str] = None,
            api_key : Optional[str] = None,
            organization : Optional[str] = None,
            limit : int = 10,
    ):
        """
        Searches the collection

        Example:
        embeddings.search(
            query = "Hello, world!"
        )

        Args:
            query (Union[str, List[str]]): The query to search for.
            model (Union[str, EmbeddingModel]): The model to use.
            base_url (Optional[str]): The base URL to use.
            api_key (Optional[str]): The API key to use.
            organization (Optional[str]): The organization to use.
            limit (int): The limit of results to return.
        """
        
        # create quick query embedding
        from ..nlp.embedder import embedding

        if isinstance(query, str):
            query = [query]

        query_embeddings = []

        for q in query:    
            try:
                query_embeddings.append(embedding(
                    q, model=model,
                    dimensions=self.dimensions,
                    base_url=base_url,
                    api_key=api_key,
                    organization=organization
                ))
            except Exception as e:
                raise XNANOException(f"Failed to get embedding for query {q}: {e}") from e
            
        results = []

        # run search
        try:
            try:
                for qe in query_embeddings:
                    result = self.client.search(
                        collection_name = self.collection_name,
                        query_vector = qe,
                        limit = limit,
                        with_payload = True,
                        with_vectors = True
                    )
                    try:
                        results.extend([
                            {   
                                "id": hit.id,
                                "text": hit.payload.pop("text", ""),  # Remove text from payload after extracting it
                                "metadata": hit.payload,  # Now payload doesn't include text
                                "score": hit.score
                            } for hit in result
                        ])
                    except Exception as e:
                        raise XNANOException(f"Failed to parse search results: {e}") from e
                    
            except Exception as e:
                raise XNANOException(f"Failed to run search: {e}") from e
            
        except Exception as e:
            raise XNANOException(f"Failed to search collection: {e}") from e

        return results
    

    def query(
            self,
            query : Union[str, List[str]],
            limit : int = 10,
    ):
        """
        Queries the memory

        Example:
        embeddings.query(
            query = "Hello, world!"
        )

        Args:
            query (Union[str, List[str]]): The query to search for.
            limit (int): The limit of results to return.
        """
        
        try:
            return self.client.query_batch(
                collection_name = self.collection_name,
                query_texts = query,
                limit = limit
            )
        except Exception as e:
            raise XNANOException(f"Failed to query collection: {e}") from e
        

    def _build_context(self, messages: MessageType, generate_queries: Optional[bool], model: ChatModel, api_key: Optional[str], base_url: Optional[str], organization: Optional[str], limit: int) -> str:
        from pydantic import BaseModel
        from ..pydantic import patch
        
        @patch
        class Queries(BaseModel):
            queries: List[str]

        instructions = (
            "Based on the following conversation, or query; generate a list of 3-5 queries"
            "that would bring up the most relevant or requested information, in the context of the conversation."
            "\n\n"
            "Instructions: \n"
            "- The queries should optimized for retrieval from a vector database."
            "- The queries should be specific to the conversation."
            "- The queries should be diverse, but related to the overall theme of the conversation or request."
        )

        context = []

        if generate_queries:
            if isinstance(messages, str):
                instructions = {"role": "user", "content": f"{instructions}\n\nQuery: {messages}"}
            elif isinstance(messages, list):
                messages = messages[-5:]
                for message in messages:
                    if isinstance(message, dict):
                        context.append(message.get("content", ""))
                    elif isinstance(message, str):
                        context.append(message)
                instructions = {"role": "user", "content": f"{instructions}\n\nConversation: {context}"}

            try:
                queries = Queries.model_generate(
                    messages=instructions,
                    model=model,
                    process="batch",
                    api_key=api_key,
                    base_url=base_url,
                    organization=organization,
                    n=1
                )
            except Exception as e:
                raise XNANOException(f"Failed to generate queries: {e}") from e

            query_results = []
            for query in queries.queries:
                query_results = self.search(query, limit=limit)
                context.extend(query_results)

            context_string = "Relevant Context: \n"
            for result in context:
                context_string += f"- {result['text']}\n"
            context_string += "The above context is provided to help generate a response that is relevant to the conversation or query."
        else:
            if isinstance(messages, str):
                query_results = self.search(messages, limit=limit)
            elif isinstance(messages, list):
                if messages and isinstance(messages[-1], dict) and messages[-1].get("role") == "user":
                    query_results = self.search(messages[-1].get("content", ""), limit=limit)

            context_string = "Relevant Context: \n"
            for result in query_results:
                context_string += f"- {result['text']}\n"
            context_string += "The above context is provided to help generate a response that is relevant to the conversation or query."

        return context_string


    def completion(
            self,
            messages: MessageType,
            model: ChatModel = "gpt-4o-mini",
            context: Optional[Context] = None,
            mode: Optional[InstructorMode] = None,
            response_model: Optional[ResponseModelType] = None,
            response_format: Optional[ResponseModelType] = None,
            tools: Optional[List[ToolType]] = None,
            run_tools: Optional[bool] = None,
            tool_choice: Optional[ToolChoice] = None,
            parallel_tool_calls: Optional[bool] = None,
            api_key: Optional[str] = None,
            base_url: Optional[str] = None,
            organization: Optional[str] = None,
            n: Optional[int] = None,
            timeout: Optional[Union[float, str, httpx.Timeout]] = None,
            temperature: Optional[float] = None,
            top_p: Optional[float] = None,
            stream_options: Optional[dict] = None,
            stop=None,
            max_completion_tokens: Optional[int] = None,
            max_tokens: Optional[int] = None,
            modalities: Optional[List[ChatCompletionModality]] = None,
            prediction: Optional[ChatCompletionPredictionContentParam] = None,
            audio: Optional[ChatCompletionAudioParam] = None,
            presence_penalty: Optional[float] = None,
            frequency_penalty: Optional[float] = None,
            logit_bias: Optional[dict] = None,
            user: Optional[str] = None,
            seed: Optional[int] = None,
            logprobs: Optional[bool] = None,
            top_logprobs: Optional[int] = None,
            deployment_id=None,
            extra_headers: Optional[dict] = None,
            functions: Optional[List] = None,
            function_call: Optional[str] = None,
            api_version: Optional[str] = None,
            model_list: Optional[list] = None,
            stream: Optional[bool] = None,
            return_messages: Optional[bool] = None,
            verbose: Optional[bool] = None,
            generate_queries: Optional[bool] = None,
            limit: int = 10,
    ):
        from ..completions import completion
        
        context_string = self._build_context(messages, generate_queries, model, api_key, base_url, organization, limit)

        if context:
            context_string += f"\n\n{context}"

        try:
            return completion(
                messages=messages,
                stream=stream,
                model=model,
                context=context_string,
                api_key=api_key,
                base_url=base_url,
                organization=organization,
                n=n,
                timeout=timeout,
                temperature=temperature,
                top_p=top_p,
                return_messages=return_messages,
                verbose=verbose,
                mode=mode,
                response_model=response_model,
                response_format=response_format,
                tools=tools,
                run_tools=run_tools,
                tool_choice=tool_choice,
                parallel_tool_calls=parallel_tool_calls,
                max_completion_tokens=max_completion_tokens,
                max_tokens=max_tokens,
                modalities=modalities,
                prediction=prediction,
                audio=audio,
                presence_penalty=presence_penalty,
                frequency_penalty=frequency_penalty,
                logit_bias=logit_bias,
                user=user,
                seed=seed,
                logprobs=logprobs,
                top_logprobs=top_logprobs,
                deployment_id=deployment_id,
                extra_headers=extra_headers,
                functions=functions,
                function_call=function_call,
                api_version=api_version,
                model_list=model_list,
            )
        except Exception as e:
            raise XNANOException(f"Failed to generate completion: {e}") from e

        
    async def acompletion(
            self,
            messages: MessageType,
            model: ChatModel = "gpt-4o-mini",
            context: Optional[Context] = None,
            mode: Optional[InstructorMode] = None,
            response_model: Optional[ResponseModelType] = None,
            response_format: Optional[ResponseModelType] = None,
            tools: Optional[List[ToolType]] = None,
            run_tools: Optional[bool] = None,
            tool_choice: Optional[ToolChoice] = None,
            parallel_tool_calls: Optional[bool] = None,
            api_key: Optional[str] = None,
            base_url: Optional[str] = None,
            organization: Optional[str] = None,
            n: Optional[int] = None,
            timeout: Optional[Union[float, str, httpx.Timeout]] = None,
            temperature: Optional[float] = None,
            top_p: Optional[float] = None,
            stream_options: Optional[dict] = None,
            stop=None,
            max_completion_tokens: Optional[int] = None,
            max_tokens: Optional[int] = None,
            modalities: Optional[List[ChatCompletionModality]] = None,
            prediction: Optional[ChatCompletionPredictionContentParam] = None,
            audio: Optional[ChatCompletionAudioParam] = None,
            presence_penalty: Optional[float] = None,
            frequency_penalty: Optional[float] = None,
            logit_bias: Optional[dict] = None,
            user: Optional[str] = None,
            seed: Optional[int] = None,
            logprobs: Optional[bool] = None,
            top_logprobs: Optional[int] = None,
            deployment_id=None,
            extra_headers: Optional[dict] = None,
            functions: Optional[List] = None,
            function_call: Optional[str] = None,
            api_version: Optional[str] = None,
            model_list: Optional[list] = None,
            stream: Optional[bool] = None,
            return_messages: Optional[bool] = None,
            verbose: Optional[bool] = None,
            generate_queries: Optional[bool] = None,
            limit: int = 10,
    ):
        from ..completions import acompletion
        
        context_string = self._build_context(messages, generate_queries, model, api_key, base_url, organization, limit)

        if context:
            context_string += f"\n\n{context}"

        try:
            return await acompletion(
                messages=messages,
                stream=stream,
                model=model,
                context=context_string,
                api_key=api_key,
                base_url=base_url,
                organization=organization,
                n=n,
                timeout=timeout,
                temperature=temperature,
                top_p=top_p,
                return_messages=return_messages,
                verbose=verbose,
                mode=mode,
                response_model=response_model,
                response_format=response_format,
                tools=tools,
                run_tools=run_tools,
                tool_choice=tool_choice,
                parallel_tool_calls=parallel_tool_calls,
                max_completion_tokens=max_completion_tokens,
                max_tokens=max_tokens,
                modalities=modalities,
                prediction=prediction,
                audio=audio,
                presence_penalty=presence_penalty,
                frequency_penalty=frequency_penalty,
                logit_bias=logit_bias,
                user=user,
                seed=seed,
                logprobs=logprobs,
                top_logprobs=top_logprobs,
                deployment_id=deployment_id,
                extra_headers=extra_headers,
                functions=functions,
                function_call=function_call,
                api_version=api_version,
                model_list=model_list,
            )
        except Exception as e:
            raise XNANOException(f"Failed to generate completion: {e}") from e