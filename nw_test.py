import smbclient

# Optional - specify the default credentials to use on the global config object
smbclient.ClientConfig(username='Administrator', password='2292')

# Optional - register the credentials with a server (overrides ClientConfig for that server)
#/smbclient.register_session("pi", username="Administrator", password="2292")

#/smbclient.mkdir(r"\\server\share\directory", username="user", password="pass")

#/with smbclient.open_file(r"\\server\share\directory\file.txt", mode="w") as fd:
  #/  fd.write(u"file contents")



#/fh = opener.open('pi://d/PVDataLog/2022_09_12.CSV""')



#/import smbclient

#/smb = smbclient.SambaClient(server="pi", share="MYSHARE",
#/                                username='Administrator', password='2292', domain='baz')
