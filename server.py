import web
import time
urls = (
    '/(.*)', 'hello'
)
app = web.application(urls, globals())

counter = 0

class hello:        
    def GET(self, name):
        global counter
        counter = counter + 1
        if not name:
            name = 'World'
        return 'Hello, ' + name + '!' + str(counter)

if __name__ == "__main__":
    app.run()
