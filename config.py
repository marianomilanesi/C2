from pysxm import ComplexType
import base64

class configuration(ComplexType):
    pass

def install():
    config = configuration()
    print('Insert github credentials:')
    config.username = input('username: ')
    password = input('password: ')
    config.token = str(base64.b64encode((config.username + ':' + password).encode('utf-8')), "utf-8")
    proxy = input('Use http proxy?(y/n)')
    if proxy == 'y':
        config.proxy = 'True'
        config.proxyhost = input('Insert proxy host: ')
        config.proxyport = input('Insert proxy port: ')
    config.save('config.xml')

if __name__ == '__main__':
    install()