class Label:
    def __init__(
            self,
            widget_factory,
            text: str,
    ):
        self.__wf = widget_factory
        self.__label = self.__wf.get("label")\
                            .set_text(text)


