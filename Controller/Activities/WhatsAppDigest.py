class WhatsAppDigest():
    def __init__(self):

        pass

    def execute(self, controller):
        message_digest = controller.whats_app_model.whats_app_storage.get_messages()
        controller.whats_app_model.whats_app_storage.clear_messages()
        for message in message_digest:
            controller.whats_app_writer.write(message)