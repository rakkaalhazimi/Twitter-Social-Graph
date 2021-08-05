# Std Libraries
import json
from collections import namedtuple
from itertools import chain
from operator import length_hint

# Third-party Libraries
from pyvis.network import Network


# Global variables
ME = "Rakka"
MY_COLOR = "slategray"
group_colors = {1: "#8BE718", 2: "#188BE7", 3: "#E7188B", 4: MY_COLOR}


Friend = namedtuple("Friend", "name, is_directed")

with open("friends.json", "rt") as file:
    records = json.load(file)


def get_friends(records):

    followers = {friend["name"] for friend in records["followers"]}
    following = {friend["name"] for friend in records["friends"]}

    return followers, following


def get_relations(followers, following):
    mutual = following.intersection(followers)  # Follow each other
    fans = followers.difference(following)      # Follow you but you don't follow them back
    favorite = following.difference(followers)  # Followed by you but they don't follow back

    return mutual, fans, favorite


def social_report(followers, following):
    mutual, fans, favorite = get_relations(followers, following)

    reports = f"""
    Followers counts : {len(followers)}
    Following counts : {len(following)} 
    Mutual counts    : {len(mutual)}
    Fans counts      : {len(fans)}
    Favorite counts  : {len(favorite)}
    """

    print(reports)


def edge_creation(mutual, fans, favorite):
    edges = []

    for person in mutual:
        edges.extend([(ME, person), (person, ME)])

    for person in fans:
        edges.append((person, ME))

    for person in favorite:
        edges.append((ME, person))

    return edges



def main():
    # Get followers and following
    followers, following = get_friends(records)

    # Get mutual, fans and favorite
    mutual, fans, favorite = get_relations(followers, following)

    # Create nodes containing your friends names (including yourself)
    nodes = [person for person in chain(mutual, fans, favorite)]
    nodes.append(ME)

    # Create edge with the respect of relationship
    edges = edge_creation(mutual, fans, favorite)

    # Define colors and groups
    groups = [group for group in chain((1 for i in mutual),
                                       (2 for j in fans),
                                       (3 for k in favorite),
                                       (4 for l in range(1)))]  # group 4 = myself
    colors = [group_colors[i] for i in groups]

    # Build social network graph
    graph = Network(width="100%", height="100%", bgcolor='#222222', font_color='white')
    graph.barnes_hut(gravity=-10000, damping=0.2)
    graph.add_nodes(nodes, color=colors)
    graph.add_edges(edges)

    graph.save_graph("social_network.html")

    return graph



if __name__ == '__main__':
    main()
