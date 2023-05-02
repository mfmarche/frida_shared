import codecs

from clang import *
from clang.cindex import *
import sys
import os
#Config.set_library_file("C:\\Program Files\\LLVM\\bin\\libclang.dll")
#Config.set_library_file("/usr/lib/llvm-11/lib/libclang.so.1")
library_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'native')

hmap={}
hname="frida-core.h"
hcall="import.c"

dep=[
    "__va_start",
    "_GLIB_",
    "json_",
    "g_",
    "gio_",
    "glib_",
    "G_",
    "gobject_",
    "_g_",
    "atexit",
]
funcs=[
    "g_bytes",
    "frida_init",
    "frida_device_manager_new",
    "frida_device_manager_close",
    "frida_shutdown",
    "frida_deinit",
    "g_main_loop_new",
    "frida_device_manager_enumerate_devices_sync",
    "frida_device_list_size",
    "frida_device_list_get",
    "frida_device_get_name",
    "frida_device_get_dtype",
    "frida_device_attach_sync",
    "frida_session_create_script_sync",
    "frida_script_load_sync",
    "g_main_loop_is_running",
    "g_signal_connect_data",
    "g_main_loop_run",
    "frida_script_unload_sync",
    "frida_session_detach_sync",
    "frida_device_manager_close_sync",
    "frida_unref",
    "frida_script_post_sync",
    "g_clear_object",
    "g_object_unref",
    "g_ref_string_length",
    "g_ref_string_release",
    "g_utf8_strlen",
    "g_strlen",
    "g_signal_connect_data",
    "g_signal_handler_disconnect",
    "g_error_free",
    "g_free",
    "g_io_stream_close",
    "g_input_stream_read_bytes",
    "g_output_stream_write_bytes",
    "g_output_stream_write_all",
    "g_input_stream_read_all",
    "g_io_stream_is_closed",
    "g_io_stream_get_input_stream",
    "g_io_stream_get_output_stream",
    "g_io_stream_has_pending",
    "g_io_stream_clear_pending",
    "g_input_stream_close",
    "g_output_stream_close",
    "g_bytes_get_data",
    "g_object_ref",
    "g_hash_table_unref",
    "g_hash_table_ref",
    "g_hash_table_iter_init",
    "g_hash_table_iter_next",
    "g_variant_is_of_type",
    "g_variant_get_string",
    "g_variant_get_int64",
    "g_variant_get_boolean",
    "g_variant_get_variant",
    "g_variant_get_fixed_array",
    "g_variant_iter_next_value",
    "g_variant_get_child_value",
    "g_variant_unref",
    "g_variant_iter_init",
    "g_variant_type_new",
    "g_variant_type_free",
    "g_variant_iter_new",
    "g_variant_iter_free",
    "g_variant_get_type_string"
]

depstruct=[
    "Json",
]
def indep(_funcname:str):
    for it in dep:
        if _funcname.startswith(it)==True:
            return True
    return False
def infuncs(_funcname:str):
    for it in funcs:
        if _funcname.startswith(it)==True:
            return True
    return False

def main():
    index = Index.create()
    root = index.parse(hname)


    f = codecs.open(hcall, "w")
    f1 = codecs.open("frida.map", "w")
    genCallHead(root.cursor,f,f1)
    genCalls(root.cursor,f,f1)
    genMyCall("_frida_g_strlen",f,f1)
    genMyCall("_frida_g_error_get_message",f,f1)
    genMyCall("_frida_g_error_get_code",f,f1)
    genMyCall("_frida_g_hash_table_iter_new",f,f1)
    genMyCall("_frida_g_hash_table_iter_free",f,f1)
    genCallFoot(root.cursor,f,f1)
    f.close()
    f1.close()
    print("Agilicus")


def genCalls(node:Cursor,_f,_f1):
    for it in node.get_children():#type:Cursor
        #or str(it.spelling) in funcs
        if infuncs(it.spelling)==True or (it.kind==CursorKind.FUNCTION_DECL and (indep(it.spelling)==False)  and str(it.location.file)==hname):
            if (it.spelling in hmap)==False:
                hmap[it.spelling]=it.spelling
                print("Agilicus:{} {}".format(it.spelling,it.type.spelling))
                _f.write("    IMPORT({});\n".format(it.spelling))
                _f1.write("        {};\n".format(it.spelling))
        genCalls(it,_f,_f1)
def genMyCall(fn,_f,_f1):
    _f1.write("        {};\n".format(fn))
def genCallHead(node,_f,_f1):
    _f.writelines("#include \"library.h\"\n")
    _f.writelines("#include <stdio.h>\n")
    _f.writelines("#define IMPORT(fn) printf(\"%p\",&fn)\n")
    _f.writelines("void ____Imp____(){\n")
    _f1.writelines("LIBFOO_1.0 {\n")
    _f1.writelines("    global:\n")

def genCallFoot(node,_f,_f1):
    _f.writelines("}\n")
    _f1.writelines("    local:\n")
    _f1.writelines("        *;\n")
    _f1.writelines("};\n")
if __name__ == '__main__':
    main()
