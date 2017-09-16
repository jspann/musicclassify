# import remix
import httplib, urllib, base64
import json
import ast
import operator #for finding largest value in dict

emotionheaders = {}#keys for the microsoft emotion api

faceheaders = {}#keys for the microsoft face api

params = urllib.urlencode({})

# Replace the example URL below with the URL of the image you want to analyze.
body = "{ 'url': 'http://jspann.me/jspann.png' }"

##File constants
KEY_FILE = "keys.conf"


def getImageSentiment(imageurlDict):#emotion API
	try:
		# NOTE: You must use the same region in your REST call as you used to obtain your subscription keys.
		#For example, if you obtained your subscription keys from westcentralus, replace "westus" in the 
		#URL below with "westcentralus".
		conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
		conn.request("POST", "/emotion/v1.0/recognize?%s" % params, imageurlDict, emotionheaders)
		response = conn.getresponse()
		data = response.read()
		conn.close()

		#converts unicode text to a dict for usage
		d = ast.literal_eval(data)[0]
		return max(d['scores'].iteritems(), key=operator.itemgetter(1))[0]#returns the sentiment in the image
		
	except Exception as e:
		print("[Errno {0}] {1}".format(e.errno, e.strerror))
	return

def getNumFaces():#face API
	# Replace the subscription_key string value with your valid subscription key.

	# Replace or verify the region.
	#
	# You must use the same region in your REST API call as you used to obtain your subscription keys.
	# For example, if you obtained your subscription keys from the westus region, replace 
	# "westcentralus" in the URI below with "westus".
	#
	# NOTE: Free trial subscription keys are generated in the westcentralus region, so if you are using
	# a free trial subscription key, you should not need to change this region.
	uri_base = 'westcentralus.api.cognitive.microsoft.com'

	# Request parameters.
	params = urllib.urlencode({
		'returnFaceId': 'true',
		'returnFaceLandmarks': 'false',
		'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
	})

	# The URL of a JPEG image to analyze.
	body = "{'url':'https://upload.wikimedia.org/wikipedia/commons/c/c3/RH_Louise_Lillian_Gish.jpg'}"

	try:
		# Execute the REST API call and get the response.
		conn = httplib.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
		conn.request("POST", "/face/v1.0/detect?%s" % params, body, faceheaders)
		response = conn.getresponse()
		data = response.read()

		# 'data' contains the JSON data. The following formats the JSON data for display.
		parsed = json.loads(data)
		print ("Response:")
		print (json.dumps(parsed, sort_keys=True, indent=2))
		conn.close()

	except Exception as e:
		print("[Errno {0}] {1}".format(e.errno, e.strerror))


def getKeys(mykeyfile):
	with open(mykeyfile) as data_file:    
		keydata = json.load(data_file)

	global headers
	emotionheaders['Content-Type'] = keydata['msftEmotionContentType']
	emotionheaders['Ocp-Apim-Subscription-Key'] = keydata['msftEmotionSubscriptionKey']

	global faceheaders
	faceheaders['Content-Type'] = keydata['msftFaceContentType']
	faceheaders['Ocp-Apim-Subscription-Key'] = keydata['msftFaceSubscriptionKey']
	

print getKeys(KEY_FILE)
print getImageSentiment(body)
print getNumFaces()