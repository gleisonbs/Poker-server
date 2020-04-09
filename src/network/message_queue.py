import queue

class MessageQueue:
    msg_queue = queue.Queue()
    @staticmethod
    def publish(message):
        MessageQueue.msg_queue.put(message)

    @staticmethod
    def get():
        return MessageQueue.msg_queue.get()

    @staticmethod
    def empty():
        return MessageQueue.msg_queue.empty()