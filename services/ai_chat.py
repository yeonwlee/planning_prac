from dotenv import load_dotenv
from langchain.chat_models import ChatOllama, ChatOpenAI
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory



HISTORY_STORAGE= {}

valid_models = {'llama3.1', 'gpt-4o-mini', 'gpt-4o'}

# API키 불러오기
load_dotenv()

class CustomChatBot():
    def __init__(self, kind_of_model:str, model_name:str, prompt_concept:str, detail_prompt:str='', temperature:float=0.1, history:bool=True) -> None:
        assert kind_of_model in valid_models, f'모델의 종류는 {valid_models} 중 선택하세요'
        
        self.model_name = model_name
        
        # 1. 모델 생성
        if kind_of_model == 'llama3.1':
            self.model = ChatOllama(model=kind_of_model, temperature=temperature)
        elif kind_of_model in {'gpt-4o-mini', 'gpt-4o'}:
            self.model = ChatOpenAI(model=kind_of_model, temperature=temperature)
        
        # 내용을 저장하는 경우
        if history:
            # 2. 프롬프트 만들기
            self.chat_prompt = ChatPromptTemplate.from_messages(
                [
                    SystemMessagePromptTemplate.from_template(f'당신은 {prompt_concept} 에 대한 전문가입니다. \
                                                                {prompt_concept}에 대해서만 답변합니다. {detail_prompt}'),
                    HumanMessagePromptTemplate.from_template('{question}'),
                    MessagesPlaceholder(variable_name='history')
                ]
            )
            # 3. 모델+프롬프트 연결 체인 만들기
            self.chat_chain = (
                RunnableWithMessageHistory(
                    self.chat_prompt | self.model,
                    self._get_session_history,
                    input_messages_key="question",
                    history_messages_key="history",
                )
            )
        else:
            # 2. 프롬프트 만들기
            self.chat_prompt = ChatPromptTemplate.from_messages(
                [
                    SystemMessagePromptTemplate.from_template(f'당신은 {prompt_concept} 에 대한 전문가입니다. \
                                                                {prompt_concept}에 대해서만 답변합니다. {detail_prompt}'),
                    HumanMessagePromptTemplate.from_template('{question}'),
                ]
            )
            # 3. 모델+프롬프트 연결 체인 만들기
            self.chat_chain = self.chat_prompt | self.model
     
    
    def _get_session_history(self, session_id: str) -> ChatMessageHistory:
        if session_id not in HISTORY_STORAGE:
            HISTORY_STORAGE[session_id] = {}
        if self.model_name not in HISTORY_STORAGE[session_id]:
            HISTORY_STORAGE[session_id][self.model_name] = ChatMessageHistory()
        return HISTORY_STORAGE[session_id][self.model_name]
    

    def _get_available_params(self) -> tuple:
        if isinstance(self.chat_chain, RunnableWithMessageHistory):
            return {'question': ''}, {'configurable': {"session_id": ''}}
        return {'question': ''}, None
    
    
    def exec(self, chat:str, user_id:str) -> str:
        session_id = user_id  # 단순화된 세션 ID 사용 (여기서는 user_id를 사용)
        
        param, config = self._get_available_params()
        param['question'] = chat
        if config is not None:
            config['configurable']['session_id'] = session_id
            response = self.chat_chain.invoke(param, config=config).content
        else:
            response = self.chat_chain.invoke(param).content
            
        # AI의 응답 저장
        return response
    
