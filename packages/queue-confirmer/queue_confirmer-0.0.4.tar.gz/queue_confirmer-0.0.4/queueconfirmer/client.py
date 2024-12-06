import socket

class ChangeableList:
    def __init__(self, items=[]):
        # Initialize with a list of items or an empty list
        self.items = items
        self.ip = None
        self.port = None

    def set_host(self, HOST, PORT):
        set.ip = HOST
        set.port = PORT


    def add_item(self, item):
        """Add an item to the list."""
        self.items.append(item)

    def send_items(self):
        c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            #Connects to HOST, PORT
        c.connect((self.ip, self.port))


        while True:

            if self.items:
                c.send(str(self.items[0]).encode('utf8'))

                # Wait for acknowledgment from the server
                data = c.recv(1024)
                conf = data.decode('utf8')
                print("Server:", conf)

                # Pop the first element after receiving confirmation
                self.items.pop(0)

        # Will print "End of queue!" when data is complete (server side)
        print("End of queue!")

    # Ends the server connection
    def end_trip(self):
        self.add_item("endtrip")

if __name__ == "__main__":
    obj = ChangeableList()
    obj.add_item(6)
    obj.add_item(4)
    obj.add_item(6)
    obj.add_item(8)
    obj.add_item("raid")
    obj.end_trip()
    obj.send_items()