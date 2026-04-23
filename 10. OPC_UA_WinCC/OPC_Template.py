import time
from opcua import ua, Server

server = Server()
server.set_endpoint("opc.tcp://0.0.0.0:4841/freeopcua/server/")
server.set_server_name("Python OPC UA Server")

idx = server.register_namespace("http://python.opcua.server")
obj = server.get_objects_node().add_object(idx, "MyObject")

value_1 = 0
value_2 = 100
value_3 = 0
value_4 = 0

tag1 = obj.add_variable(idx, "My_Value_1", ua.Variant(value_1, ua.VariantType.Int32))
tag2 = obj.add_variable(idx, "My_Value_2", ua.Variant(value_2, ua.VariantType.Int32))
tag3 = obj.add_variable(idx, "My_Value_3_From_SCADA", ua.Variant(value_3, ua.VariantType.Int32))
tag4 = obj.add_variable(idx, "My_Value_4_From_SCADA", ua.Variant(value_4, ua.VariantType.Int32))

tag1.set_writable()
tag2.set_writable()
tag3.set_writable()
tag4.set_writable()

server.start()
while True:
    value_1 += 1
    value_2 += 2

    tag1.set_value(ua.Variant(value_1, ua.VariantType.Int32))
    tag2.set_value(ua.Variant(value_2, ua.VariantType.Int32))

    scada_val_1 = tag3.get_value()
    scada_val_2 = tag4.get_value()

    print(f"Write -> V1={value_1}, V2={value_2}")
    print(f"Read  <- SCADA1={scada_val_1}, SCADA2={scada_val_2}")

    time.sleep(1)