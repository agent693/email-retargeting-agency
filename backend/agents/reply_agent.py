class ReplyAgent:
    def handle_replies(self, clicked_results):
        return [item["email"] for item in clicked_results]
