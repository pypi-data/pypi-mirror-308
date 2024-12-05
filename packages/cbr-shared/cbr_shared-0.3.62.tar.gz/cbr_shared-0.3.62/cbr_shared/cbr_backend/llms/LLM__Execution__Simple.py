import requests
from cbr_shared.schemas.data_models.llm_chat.LLMs__Chat_Completion  import LLMs__Chat_Completion
from osbot_utils.base_classes.Type_Safe                             import Type_Safe
from osbot_utils.helpers.Random_Guid                                import Random_Guid

URL__LLM__COMPLETION__PROXY = "https://osbot-llms.dev.aws.cyber-boardroom.com/chat/completion"

DEFAULT__LLM__COMPLETION__PROXY__SELECTED_PLATFORM = "Groq (Free)"
DEFAULT__LLM__COMPLETION__PROXY__SELECTED_PROVIDER = "1. Meta"
DEFAULT__LLM__COMPLETION__PROXY__SELECTED_MODEL    = "llama-3.2-11b-vision-preview"

class LLM__Execution__Simple(Type_Safe):
    chat_thread_id    : Random_Guid
    selected_platform : str = DEFAULT__LLM__COMPLETION__PROXY__SELECTED_PLATFORM
    selected_provider : str = DEFAULT__LLM__COMPLETION__PROXY__SELECTED_PROVIDER
    selected_model    : str = DEFAULT__LLM__COMPLETION__PROXY__SELECTED_MODEL
    stream            : bool = False
    target_server     : str = URL__LLM__COMPLETION__PROXY
    system_prompts    : list
    images            : list

    def execute(self, user_prompt):
        llm_chat_completion = self.llm_chat_completion(user_prompt)
        request_body        = llm_chat_completion.json()
        response = requests.post(self.target_server, json=request_body)
        return response.text

    def llm_chat_completion(self, user_prompt):
        user_data      = { "selected_platform": self.selected_platform ,
                           "selected_provider": self.selected_provider ,
                           "selected_model"   : self.selected_model    }

        kwargs  = dict(user_prompt    = user_prompt         ,
                       system_prompts = self.system_prompts ,
                       images         = self.images         ,
                       chat_thread_id = self.chat_thread_id ,
                       user_data      = user_data           ,
                       stream         = self.stream         )

        return LLMs__Chat_Completion(**kwargs)