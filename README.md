# mediaPutter
A simple vanilla python3 app to move files from one place to another. Really just a wrapper for SCP with some trickery on top.

Requires all machines to have SSH Key Authorization completed and be accepting SFTP connections. 

To Use. Run from CLI in repository folder
> python3 mediaPutter.py

Selecting Media:
Either select a local folder with "Select Media Folder" or use the "NAS Location" button to configure a remote file share source.
[If you've already configured a NAS Location and your source files are not appearing, try toggling the 'Use NAS' checkbox]

The list of files in the 'Media Files' box are the files found in the source. To ignore certain files simply select them.

The Filter is to use Regular Expressions on your naming schema to derive a destination ID. 
ID Size will give the amount of digits to be searched for. 
ID Mod will add a positive or negative number to the result.

Media Per Filtered Server is a list of files distributed per found ID.

Destination Folder: The final destination folder. This folder does not have to exist, the program will make it.
Destination Path: Path to the Destination Folder
IP Schema: user@ip

Any of the above can use the keyword $ID. This will insert the given server ID into each destination. 

Overwrite Files will transfer files regardless of if they exist or not.

## ----Example-----

My Servers are 
- 1 = 192.168.1.101 
- 2 = 192.168.1.102
- 4 = 192.168.1.104

Select Media Folder containing:
- 001.File 1-Server 1.mov
- 002.File 2-Server-1.mov
- 003.File3-Server2.mov
- 004.File 4-Server 4.mov
- 100.Song.aac

I only want to move .mov files so I select the .aac file from the list. It will disappear from the 'Media Per Filtered Server' list.

I want each .mov file to go to the respective Server. [1, 2, 4]
My filter would look like \d.txt, ID Size: 1, ID Mod: 0.

* 1 <---SERVER ID
    - 001.File 1-Server 1.txt 
    - 002.File 2-Server-1.txt
* 2
    - 003.File3-Server2.txt
* 4
    - 004.File 4-Server 4.txt

But this sets the ID as a single digit and my server ID in the schema is 3 digits. So ID Mod wants to be 100.
* 101
    - 001.File 1-Server 1.txt
    - 002.File 2-Server-1.txt
* 102
   - 003.File3-Server2.txt
* 104
    - 004.File 4-Server 4.txt

Destination Folder: 001.AwesomeExample

Destination Path: /Applications/Mbox/Media/ (Note the / at the end!)

IP Schema prg@192.168.1.$ID

^^Note the $ID. This sets files in your server 1 to go to prg@192.168.1.101, which is how they are addressed.

Now when I hit start transfer each file for each server will be copied.
