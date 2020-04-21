# id3fix

1.Install Deps
  $apt install python3-venv

2.Create virtual env
  $python3 -m venv env

3.Active virtual env
  $source id3fix/env/bin/activate
  
4.Install requirements
  $pip3 install -r requirements.txt

5.Edit id3fix.py :
	ENCCODE_FROM and DECODE_TO to Default Encoding and Change rating.changeEmail in id3fix.py Params

6.Run :
	$:./id3fix.py [rating|encode] /Extend/Music 
