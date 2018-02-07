class ObjectClass:
    def __init__(self,name,object_id,tracking_frames):
        self.__name = name
        self.__object_id = object_id
        self.__tracking_frames = tracking_frames

    def get_info(self):
        return [self.__name,self.__object_id,self.__tracking_frames]

if __name__ == '__main__':
    pass
