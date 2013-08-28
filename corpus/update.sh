#!/bin/bash

# CREATE VOCABULARY FILE FOR UPDATING
echo ">> Generating vocabulary file..."
#for file in `ls ../scopes`; do
#	for word in `cat ../scopes/$file | grep -oE '".+".+:' | cut -d ':' -f 1 | tr -d '"'`
#		do echo $word >> vocab
#	done
#done

for word in `cat ../scopes.py | grep -oE '".+".+:' | cut -d ':' -f 1 | tr -d '"'`
	do echo $word >> vocab
done

# SETUP URL
URL='http://www.speech.cs.cmu.edu'
echo ">> Uploading vocabulary corpus..."

# MAKE HTTP POST REQUEST TO UPLOAD SPECIFIED CORPUS FILE
RESPONSE=`curl -sL -H "Content-Type: multipart/form-data" -F "corpus=@vocab" -F "formtype=simple" $URL/cgi-bin/tools/lmtool/run/`
rm vocab

# ECHO THE CONTENTS OF THE SAVED HTTP RESPONSE, PARSE OUT THE UNIQUE URL
REF_URL=`echo $RESPONSE | grep -oE 'title[^<>]*>[^<>]+' | cut -d'>' -f2 | sed -e "s/Index of//g" | tr -d ' '`

# ECHO THE CONTENTS OF THE SAVED HTTP RESPONSE, PARSE OUT THE UNIQUE SID
REF_SID=`echo $RESPONSE | grep -oE 'b[^<>]*>[^<>]+' | cut -d'>' -f2 | awk '/[0-9]/ { print $0 }' | head -1`

# MAKE HTTP GET REQUEST TO DOWNLOAD THE GENERATED LANGUAGE MODEL, AND DICTIONARY
echo ">> Getting generated language model and dictionary..."
curl -so lm $URL$REF_URL/$REF_SID.lm
curl -so dic $URL$REF_URL/$REF_SID.dic

# FINISHED
echo ">> Language model and dictionary have been updated!"