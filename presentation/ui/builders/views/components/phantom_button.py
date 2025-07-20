class PhantomButton:
    def __init__(
            self,
            widget_factory,
            text:str
    ):
        self.__wf = widget_factory
        self.__button = self.__wf.get("button")\
            .create()\
            .set_text(text)\
            .set_style_sheet(
            """
            #ph_btn {
                color: white;
            
                padding: 10px;
                
                border-radius: 12px;
                background-color: #f7b696;
            }
            
            #ph_btn:hover {
                color: #f7b696;
            
                background-color: transparent;
                border: 2px solid #f7b696;
            }
            """
            )\
            .set_object_name("ph_btn")\
            .build()

    def get(self):
        return self.__button