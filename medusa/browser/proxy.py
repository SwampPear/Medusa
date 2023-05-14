import socket   

class Proxy:
  def __init__(self) -> None:
    pass

  def test(self) -> None:
    """
    Only used for testing during implementation.
    """
    
    hostname=socket.gethostname()   
    IPAddr=socket.gethostbyname(hostname)   
    print("Your Computer Name is:"+hostname)   
    print("Your Computer IP Address is:"+IPAddr)  