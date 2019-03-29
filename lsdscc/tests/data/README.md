# tests/data
This folder contains the sample I found in the paper where it is used to illustrate the alignment between groups of references and model response sentences and how the three metrics are computed based on that. See the `paper-illustration.png` to get an intuition of how
sentences are aligned.

- `data/`
    * `groups.json` The reference groups. It is a json list of 2 elements. The first one is constructed directly from the illustration of the paper.
    The second one is found in the testing dataset `test.group.json` sharing the same query as the first one. But please note their references are *not the same*.
    * `query.txt` The input query in plain text. There is only one instance.
    * `response.txt` The supposed model output. It is 8 sentences in one line, separated by eos token `</s>`. This is the response set in the paper's terminology.

# Responses
- Group-1
    * The Workaholics should be fun.
    * The Workaholics guys are fun.
- Group-2
    * He's also in top five by Chris Rock.
    * He has an important role.
    * I saw Anders, and he is good.
- Group-3
    * I thought he was good.
    * He is my favorite.
    * Anders annoys me.
   
# References
- Group-1
    * Rogen and Goldberg are producing a movie being acted by the Workaholics guys.   
    * I think Rogen is producing a movie from Workaholics guys, should be fun!
- Group-2
    * He's also in top five by Chris Rock.
    * He has an important role in the top five and it's hilarious.
    * He was quite in in top five, another comedy that came out recently.
    * Looks he have pretty big role in top five, the new Chris Rock movie.
- Group-3
    * When I saw Anders, I thought he was going to be a CIA analyst, especially when Rogen asked him if he was still Associate Producer.
- Group-4
    * Anders is my favorite too Blake annoys me sometimes but the show wouldn't be the same without him.