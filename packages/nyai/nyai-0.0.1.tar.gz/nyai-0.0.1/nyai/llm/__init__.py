__all__ = [
    "LLM",
    "AsyncLLM"
]

from openai.resources import Chat, AsyncChat
from openai._types import NOT_GIVEN, NotGiven

from typing import List, Dict, Any, Iterable, Optional

class BaseLLM:
    pass
   

class LLM(Chat, BaseLLM):
    def __init__(self, 
                client: Any,
                remember: bool = None,
                model: str = None,
                messages: List[dict] = None,
                system: str = None): 
        super().__init__(client)
        self.remember = remember or True
        self.messages = messages or []
        self.system = system or "You are a helpful assistant."
        self.model = model
        
    def chat(self,
             message: Dict[str, List[Any] | str] | str,
             messages: Optional[List[Dict[str, str | Any]]] = None, 
             system: Optional[str] = None,
             model: Optional[str] = None,
             lmc: bool = False,
             lmc_input: bool = False,
             lmc_output: bool = False,
             raw: bool = False,
             role: str = "user", 
             author: Optional[str] = None,
             attachments: Optional[Iterable[str] | str] = None,
             attachments_type: Optional[Iterable[str] | str] = None,
             stream: bool = False,
             max_tokens: Optional[int] = NotGiven,
             remember: bool = True, 
             schema: Optional[Dict[str, Any]] = None,
             **kwargs
             ) -> str | Dict[str, str | List[Dict[str, str]]]:
        """
        Calls the chat model with the provided parameters.

        Args:
            message (Dict[str, List[Any] | str] | str): The primary message to send, either as a string or 
                a dictionary containing content details.
            messages (Optional[List[Dict[str, str | Any]]]): A list of prior messages in the conversation context.
            system (Optional[str]): System message for model context, if any.
            model (Optional[str]): Model name or ID. Defaults to the client’s model if not specified.
            lmc (bool): Flag to enable both `lmc_input` and `lmc_output`.
            lmc_input (bool): Flag to preprocess the input message.
            lmc_output (bool): Flag to process output into LMC format.
            raw (bool): If True, returns raw response from the model.
            role (str): Role of the sender, defaults to "user".
            author (Optional[str]): Identifier for the message author.
            attachments (Optional[str]): Attachment data for the message, if any.
            attachments_type (Optional[str]): Type of attachment data.
            stream (bool): If True, enables response streaming (currently unused).
            max_tokens (Optional[int]): Maximum token limit for the model response.
            remember (bool): If True, stores the message in the conversation history.
            schema (Optional[Dict[str, Any]]): Schema for expected output structure, if applicable.

        Returns:
            str | Dict[str, str | List[Dict[str, str]]]: The content response from the model, optionally in LMC format or raw.
        """
        lmc_input, lmc_output = (True, True) if lmc else (lmc_input, lmc_output)
        message = message if lmc_input else to_lmc(message, 
                                                   attachments=attachments, 
                                                   attachments_type=attachments_type,
                                                   role=role,
                                                   author=author)
        if not (model or self.model):
            raise ValueError("Model param is missin")
        
        if system:
            system = to_send(system or self.system, role="system")
        
        if stream:
            return self.stream(message=message,
                               lmc_input=True,
                               lmc_output=lmc_output,
                               remember=remember,
                               model=model,
                               max_tokens=max_tokens,
                               raw=raw,
                               system=system)

        response = self.completions.create(
            model=model or self.model,
            messages=map(to_send, [system or self.system] + (messages or self.messages) + [message]),
            **kwargs
        )
        content = response.choices[0].message.content   
        if remember:
            self.messages += [message, to_lmc(content, role="assistant")]
            if lmc_output:
                return self.messages[-1]
        if raw:
            return response
        elif lmc_output:
            return to_lmc(content, role="assistant")
        return content
    
    def stream(self,
               message: Dict[str, List[Any] | str] | str,
               messages: Optional[List[Dict[str, str | Any]]] = None, 
               system: Optional[str] =   None,
               model: Optional[str] = None,
               lmc: bool = False,
               lmc_input: bool = False,
               lmc_output: bool = False,
               raw: bool = False,
               role: str = "user", 
               author: Optional[str] = None,
               attachments: Optional[Iterable[str] | str] = None,
               attachments_type: Optional[Iterable[str] | str] = None,
               max_tokens: Optional[int] | NotGiven = NOT_GIVEN,
               remember: bool = True,
               **kwargs):
        
        lmc_input, lmc_output = (True, True) if lmc else (lmc_input, lmc_output)
        message = message if lmc_input else to_lmc(message, 
                                                   attachments=attachments, 
                                                   attachments_type=attachments_type,
                                                   role=role,
                                                   author=author)
        if not (model or self.model):
            raise ValueError("Model param is missin")
        
        if system:
            system = to_send(system or self.system, role="system")
        
        response = self.completions.create(
            model=model or self.model,
            messages=map(to_send, [system or self.system] + (messages or self.messages) + [message]),
            stream=True,
            **kwargs
        )
        
        if remember:
            self.messages.append(message)
        
        completion = ""
        for chunk in response:
            completion += chunk.choices[0].delta.content
            if lmc_output:
                yield to_lmc(completion, role="assistant") | {"chunk": chunk.choices[0].delta.content}
            elif raw:
                yield chunk
            else:
                yield chunk.choices[0].delta.content
                 
        if remember:
            self.messages.append(to_lmc(completion, role="assistant"))

class AsyncLLM(AsyncChat, BaseLLM):
    def __init__(self, 
                client: Any,
                remember: bool = None,
                model: str = None,
                messages: List[dict] = None,
                system: str = None): 
        super().__init__(client)
        self.remember = remember or True
        self.messages = messages or []
        self.system = system or "You are a helpful assistant."
        self.model = model
        
    async def chat(self,
                   message: Dict[str, List[Any] | str] | str,
                   messages: Optional[List[Dict[str, str | Any]]] = None, 
                   system: Optional[str] = None,
                   model: Optional[str] = None,
                   lmc: bool = False,
                   lmc_input: bool = False,
                   lmc_output: bool = False,
                   raw: bool = False,
                   role: str = "user", 
                   author: Optional[str] = None,
                   attachments: Optional[Iterable[str] | str] = None,
                   attachments_type: Optional[Iterable[str] | str] = None,
                   stream: bool = False,
                   max_tokens: Optional[int] = NotGiven,
                   remember: bool = True, 
                   schema: Optional[Dict[str, Any]] = None,
                   **kwargs
                   ) -> str | Dict[str, str | List[Dict[str, str]]]:
        """
        Calls the chat model with the provided parameters.

        Args:
            message (Dict[str, List[Any] | str] | str): The primary message to send, either as a string or 
                a dictionary containing content details.
            messages (Optional[List[Dict[str, str | Any]]]): A list of prior messages in the conversation context.
            system (Optional[str]): System message for model context, if any.
            model (Optional[str]): Model name or ID. Defaults to the client’s model if not specified.
            lmc (bool): Flag to enable both `lmc_input` and `lmc_output`.
            lmc_input (bool): Flag to preprocess the input message.
            lmc_output (bool): Flag to process output into LMC format.
            raw (bool): If True, returns raw response from the model.
            role (str): Role of the sender, defaults to "user".
            author (Optional[str]): Identifier for the message author.
            attachments (Optional[str]): Attachment data for the message, if any.
            attachments_type (Optional[str]): Type of attachment data.
            stream (bool): If True, enables response streaming (currently unused).
            max_tokens (Optional[int]): Maximum token limit for the model response.
            remember (bool): If True, stores the message in the conversation history.
            schema (Optional[Dict[str, Any]]): Schema for expected output structure, if applicable.

        Returns:
            str | Dict[str, str | List[Dict[str, str]]]: The content response from the model, optionally in LMC format or raw.
        """
        lmc_input, lmc_output = (True, True) if lmc else (lmc_input, lmc_output)
        message = message if lmc_input else to_lmc(message, 
                                                   attachments=attachments, 
                                                   attachments_type=attachments_type,
                                                   role=role,
                                                   author=author)
        if not (model or self.model):
            raise ValueError("Model param is missin")
        
        if system:
            system = to_send(system or self.system, role="system")
        
        if stream:
            return self.stream(message=message,
                               lmc_input=True,
                               lmc_output=lmc_output,
                               remember=remember,
                               model=model,
                               max_tokens=max_tokens,
                               raw=raw,
                               system=system)

        response = self.completions.create(
            model=model or self.model,
            messages=map(to_send, [system or self.system] + (messages or self.messages) + [message]),
            **kwargs
        )
        content = response.choices[0].message.content   
        if remember:
            self.messages += [message, to_lmc(content, role="assistant")]
            if lmc_output:
                return self.messages[-1]
        if raw:
            return response
        elif lmc_output:
            return to_lmc(content, role="assistant")
        return content
    
    async def stream(self,
               message: Dict[str, List[Any] | str] | str,
               messages: Optional[List[Dict[str, str | Any]]] = None, 
               system: Optional[str] = None,
               model: Optional[str] = None,
               lmc: bool = False,
               lmc_input: bool = False,
               lmc_output: bool = False,
               raw: bool = False,
               role: str = "user", 
               author: Optional[str] = None,
               attachments: Optional[Iterable[str] | str] = None,
               attachments_type: Optional[Iterable[str] | str] = None,
               max_tokens: Optional[int] | NotGiven = NOT_GIVEN,
               remember: bool = True,
               **kwargs):
        
        lmc_input, lmc_output = (True, True) if lmc else (lmc_input, lmc_output)
        message = message if lmc_input else to_lmc(message, 
                                                   attachments=attachments, 
                                                   attachments_type=attachments_type,
                                                   role=role,
                                                   author=author)
        if not (model or self.model):
            raise ValueError("Model param is missin")
        
        if system:
            system = to_send(system or self.system, role="system")
        
        response = self.completions.create(
            model=model or self.model,
            messages=map(to_send, [system or self.system] + (messages or self.messages) + [message]),
            stream=True,
            **kwargs
        )
        
        if remember:
            self.messages.append(message)
        
        completion = ""
        async for chunk in response:
            completion += chunk.choices[0].delta.content
            if lmc_output:
                yield to_lmc(completion, role="assistant") | {"chunk": chunk.choices[0].delta.content}
            elif raw:
                yield chunk
            else:
                yield chunk.choices[0].delta.content
                 
        if remember:
            self.messages.append(to_lmc(completion, role="assistant"))

def to_lmc(
    message: str,
    attachments: Iterable[str] | str = [],
    attachments_type: Iterable[str] | str = "image_url",
    role: str = "user",
    author: Optional[str] = None,
    type: Optional[str] = "text"
) -> Dict[str, str | List[Dict[str, str]]]:
        
    if attachments:
        if isinstance(attachments, str):
            attachments = [attachments]
        if isinstance(attachments_type, str):
            attachments_type = [attachments_type] * len(attachments)
        
        if len(attachments) != len(attachments_type):
            raise ValueError("`attachments` and `attachments_type` must have the same length")

        attachments = [{"type": type, type: message}] + [
            {"type": att_type, att_type: {"url": att}}
            for att, att_type in zip(attachments, attachments_type)
        ]

    return {
        "role": role,
        "content": attachments or message,
        "author": author,
        "type": type
    }
    
def to_send(message: Dict[str, str | List[Dict[str, str]]] | str, 
            *args, **kwargs) -> Dict[str, str | List[Dict[str, str]]]:
    
    if isinstance(message, str): 
        message = to_lmc(message, *args, **kwargs)    
    author = f"(name: {message['author']}) " if message['author'] else ""
    
    if isinstance(message["content"], list):
        message["content"][0]["text"] = author + message['content'][0]['text']
    else:
        message["content"] = author + message['content']
    return message
