from slack_bolt import App
#  必要な要素を取得してSlackに送信して表示
def contents_to_slack(client, targets_id, praise_writing, *prise_quantity):

    client.chat_postMessage(
        channel="C025BBH57LN",
        blocks=[
            {
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": "ほめたい速報:thumbsup:",
				"emoji": True
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": mention(targets_id)
			}
		},
		{
			"type": "divider"
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": praise_writing
			}
		},
		{
			"type": "divider"
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": ":clap:ほめクラップ:clap:"
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": ":clap::clap::clap::clap::clap::clap::clap::clap::clap::clap::clap::clap::clap::clap::clap::clap::clap::clap::clap::clap::clap::clap::clap::clap::clap::clap:"
			}
		},
		{
			"type": "image",
			"title": {
				"type": "plain_text",
				"text": "homehome",
				"emoji": True
			},
			"image_url": "https://tenor.com/bfiRs.gif",
			"alt_text": "marg"
		}
        ]
    )

def mention(user_id):

	targets_id = "いつも頑張っている"

	for targets in user_id:
		targets_id += "<@" + targets + ">"

	return targets_id