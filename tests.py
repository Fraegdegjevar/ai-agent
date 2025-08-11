from functions.get_files_info import get_files_info

def test():    
    result = get_files_info("calculator", ".")
    print("Result for current directory:")
    print(result)
    print("")

    result = get_files_info("calculator", "pkg")
    print("Result for 'pkg' directory:")
    print(result)

    result = get_files_info("calculator", "/bin")
    print("Result for '/bin' directory:")
    print(result)

    result = get_files_info("calculator", "../")
    print("Result for '../' directory:")
    print(result)
    
    result = get_files_info("calculator", "foo")
    print("Result for fake '/foo' directory:")
    print(result)
    
    result = get_files_info(".", "/home/will/")
    print("Result for home directory:")
    print(result)
    
    result = get_files_info(".", ".")
    print("Result for everything in current directory inside current directory (i.e project root)")
    print(result)
    
if __name__ == "__main__":
    test()