from ..func import *
import vk_api
from vk_api.utils import get_random_id

def process_poll(event,peer_id, poll_id,str, token_bot):
    vk_session = vk_api.VkApi(token=token_bot)
    vk = vk_session.get_api()
    is_admin = vk.messages.getConversationMembers(peer_id=peer_id)["items"][0]["is_admin"]
    try:
        poll_send, mes, poll_id1 = get_poll_mes(str, is_admin, poll_id)
        vk.messages.send(
            message=mes,
            attachment = poll_send,
            random_id = get_random_id(),
            chat_id = event.chat_id
        )
        if ("-p" in str and is_admin):
            poll_id = poll_id1
            vk.messages.pin(conversation_message_id=event.obj.message['conversation_message_id']+1,
                            peer_id=event.obj.message['peer_id'])
            print(poll_id)
    except:
        pass