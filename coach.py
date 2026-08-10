from rag import retrieve_context


def get_response(question, mode):
    """
    Generate a response for the student's DSA request.
    """

    context = retrieve_context(question)

    if mode == "Learn DSA":
        prompt = f"""
        Explain the following DSA question clearly.

        Relevant knowledge:
        {context}

        Student question:
        {question}
        """

    elif mode == "Practice":
        prompt = f"""
        Help the student practice this DSA topic.
        Do not immediately provide the complete solution.

        Relevant knowledge:
        {context}

        Topic:
        {question}
        """

    elif mode == "Get Hint":
        prompt = f"""
        Give a useful hint for this DSA problem.
        Do not give the complete solution.

        Relevant knowledge:
        {context}

        Problem:
        {question}
        """

    elif mode == "View Solution":
        prompt = f"""
        Explain the solution to this DSA problem step by step.

        Relevant knowledge:
        {context}

        Problem:
        {question}
        """

    elif mode == "Code Review":
        prompt = f"""
        Review the student's code.
        Identify errors, explain them and suggest improvements.

        Relevant knowledge:
        {context}

        Student code/question:
        {question}
        """

    else:
        prompt = question

    # LLM call will be added here
    return prompt