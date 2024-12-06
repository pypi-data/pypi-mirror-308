from typing import List, Union, Literal, Optional

from collinear.BaseService import BaseService
from collinear.judge.types import VeritasNanoOutput, ConversationMessage, ConversationInput, VeritasOutput


class Veritas(BaseService):
    def __init__(self, access_token: str) -> None:
        super().__init__(access_token)

    async def question_answer(self, context: str, question: str, answer: str,
                              model_name: Literal[
                                  'veritas_nano', 'veritas'] = 'veritas_nano',
                              model_id: Optional[str] = None) -> VeritasNanoOutput | VeritasOutput:
        """
       Sends a question-answer request to the veritas judge.

       Args:
        context (str): The context of the question.
        question (str): The question to answer.
        answer (str): The answer provided.
        model_name (Literal['veritas_nano', 'veritas']): The model to use for the judgement. Default is 'veritas_nano'.
        model_id (str): The model id to use for a fine-tuned model. Default is None

       Returns:
           VeritasNanoOutput: Contains judgement and score.

       """
        response = await self.send_request('/api/v1/judge/reliability', "POST", {
            'model_name': model_name,
            'model_id': model_id,
            'type': 'qa',
            "context": context,
            "question": question,
            "answer": answer
        })
        if model_name == 'veritas_nano':
            return VeritasNanoOutput(judgement=response['judgement'], score=response['extra']['score'])
        else:
            return VeritasOutput(judgement=response['judgement'], rationale=response['extra']['rationale'])

    async def natural_language_inference(self, context: str, claim: str, model_name: Literal[
        'veritas_nano', 'veritas'] = 'veritas_nano',
                                         model_id: Optional[str] = None) -> VeritasNanoOutput | VeritasOutput:
        """
        Sends a natural language inference request to the veritas judge.

        Args:
            context (str): The context of the claim.
            claim (str): The claim to check.
            model_name (Literal['veritas_nano', 'veritas']): The model to use for the judgement. Default is 'veritas_nano'.
            model_id (str): The model id to use for a fine-tuned model. Default is None


        Returns:
            VeritasNanoOutput: Contains judgement and score.

        """
        response = await self.send_request('/api/v1/judge/reliability', "POST", {
            'model_name': model_name,
            'model_id': model_id,
            'type': 'nli',
            "context": context,
            "claim": claim
        })
        if model_name == 'veritas_nano':
            return VeritasNanoOutput(judgement=response['judgement'], score=response['extra']['score'])
        else:
            return VeritasOutput(judgement=response['judgement'], rationale=response['extra']['rationale'])

    async def conversation(self, context: str, conv_prefix: List[Union[ConversationMessage, dict]],
                           response: Union[ConversationMessage, dict],
                           model_name: Literal[
                               'veritas_nano', 'veritas'] = 'veritas_nano',

                           model_id: Optional[str] = None) -> VeritasNanoOutput | VeritasOutput:
        """
    Sends a conversation request to the Veritas judge.

    Args:
        context (str): The context of the conversation. Provide relevant background information.
        conv_prefix (List[Union[ConversationMessage, dict]]): The conversation history.
            Each message should be either a ConversationMessage object or a dict with 'role' and 'content' keys.
            Example: [{"role": "user", "content": "Hello"}, {"role": "assistant", "content": "Hi there!"}]
        response (Union[ConversationMessage, dict]): The response to be evaluated.
            Should be either a ConversationMessage object or a dict with 'role' and 'content' keys.
            Example: {"role": "assistant", "content": "How can I help you today?"}
        model_name (Literal['veritas_nano', 'veritas']): The model to use for the judgement. Default is 'veritas_nano'.
        model_id (str): The model id to use for a fine-tuned model. Default is None


    Returns:
        VeritasNanoOutput: Contains the judgement and score from the Veritas judge.

    Raises:
        ValueError: If the input data is invalid or doesn't meet the required format.

    Example:
        output = await conversation(
            context="Customer service conversation",
            conv_prefix=[{"role": "user", "content": "I have a problem with my order"}],
            response={"role": "assistant", "content": "I'm sorry to hear that. Can you provide more details?"}
        )
    """
        # NOTE: Doing this to validate input data
        input_data = ConversationInput(
            context=context,
            conversation=conv_prefix,
            response=response
        )

        response = await self.send_request('/api/v1/judge/reliability', "POST", {
            'model_name': model_name,
            'model_id': model_id,
            'type': 'conversation',
            "context": context,

            **input_data.dict()
        })
        if model_name == 'veritas_nano':
            return VeritasNanoOutput(judgement=response['judgement'], score=response['extra']['score'])
        else:
            return VeritasOutput(judgement=response['judgement'], rationale=response['extra']['rationale'])
