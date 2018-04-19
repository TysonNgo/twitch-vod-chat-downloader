from time import sleep
import json
import os
import requests
import sys

def get_time(comment):
	s = int(comment["content_offset_seconds"])
	m,s = int(s/60), int(s%60)
	h,m = int(m/60), int(m%60)

	return str(h).zfill(2)+":"+str(m).zfill(2)+":"+str(s).zfill(2)


def main():
	if len(sys.argv) not in [2, 3]:
		print("usage: python main.py <video_id> <outfile_name>")
		print("    where <video_id> is a twitch VOD video id")
		print("          <outfile_name> is optional output filename (default filename is video_id)")
		sys.exit(1)

	with open("config.json") as f:
		config = json.load(f)

	video_id = sys.argv[1]
	outfile_name = sys.argv[-1]
	base_url = "https://api.twitch.tv/v5/videos/%s/comments?" % (video_id)
	headers = {
		"Client-ID": config["client-id"]
	}

	c = []

	comments = requests.get(base_url+"content_offset_seconds=0", headers=headers)

	if not comments.ok:
		print("invalid video id or client id")
		sys.exit(1)

	comments = comments.json()
	while ("_next" in comments):
		c.extend(comments["comments"])
		for comment in comments["comments"]:
			print(get_time(comment))
		comments = requests.get(base_url+"cursor="+comments["_next"], headers=headers).json()
		sleep(0.2)

	c.extend(comments["comments"])
	for comment in comments["comments"]:
		print(get_time(comment))

	with open(config["outdir"]+os.sep+outfile_name+".json", "w") as f:
		json.dump(c, f, indent=1)

if __name__ == "__main__":
	main()