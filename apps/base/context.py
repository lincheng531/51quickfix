import settings
def settings_processor(request):
        my_dict= {
                  'DEBUG':settings.DEBUG,
                  'HOST_NAME':settings.HOST_NAME,
                  'ENV_NAME':settings.ENV_NAME,
        }
        return my_dict

