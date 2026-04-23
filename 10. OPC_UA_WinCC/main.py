from opcua import ua, Server
import time


server = Server()
server.set_endpoint("opc.tcp://0.0.0.0:4841/freeopcua/server/")
server.set_server_name("Python Powerenir")

idx = server.register_namespace('htpp://python.opcua.server')
obj = server.get_objects_node().add_object(idx, "My_Object")

value_1= 10
tag1 = obj.add_variable(idx, "Temp", ua.Variant(value_1, ua.VariantType.Int32))
tag1.set_writable()

server.start()
while True:
    value_1 += 1
    tag1.set_value(ua.Variant(value_1, ua.VariantType.Int32))
    time.sleep(1)
    print("Value: ", value_1)




