#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import networkx as nx
import heapq as hp
import time

#1

#IMPORT FROM LOCALFILE
#file_data=open("/Users/Zilbu/Documents/Studio/Algorithmic Methods/H4/reduced_dblp.json",'r')
file_data=open("/Users/Zilbu/Documents/Studio/Algorithmic Methods/H4/full_dblp.json",'r')
data = json.loads(file_data.read())
file_data.close()


conferences={}
publications={}
authors={}
G=nx.Graph()

#Parse Data
for i in data:
    conf_int=i["id_conference_int"]
    pub_int=i["id_publication_int"]
    
    #Add conference to conferences
    #Add publication to conference in conferences
    if conf_int in conferences:
        conferences[conf_int]["pub_int"].append(pub_int)
    else:
        conferences[conf_int]={"conf":i["id_conference"],"title":i["title"],"pub_int":[pub_int]}
    
    #Add publication to publications
    publications[pub_int]={"pub":i["id_publication"],"authors":[]}
    
    #Add author to authors
    #Add publication to every authour
    #Add authors to publication in publications
    for j in i["authors"]:
        aut_id=j["author_id"]
        publications[pub_int]["authors"].append(aut_id)
        if aut_id not in authors:
            authors[aut_id]={"name":j["author"],"pub":[pub_int]}
            G.add_node(aut_id) #add nodes to graph G
        else:
            authors[aut_id]["pub"].append(pub_int)

#add edges to graph G 
for p in publications.values():
    aut_list=p["authors"]
    l=len(aut_list)
    if l>1:
        for i in range(0,l-1):
            a1=aut_list[i]
            for j in range(i+1,l):
                a2=aut_list[j]
                if not G.has_edge(a1,a2):
                    pub1=authors[a1]["pub"]
                    pub2=authors[a2]["pub"]
                    
                    union=set(pub1).union(pub2)
                    inters=set(pub1).intersection(pub2)
                    w=1-len(inters)/len(union)
                    G.add_edge(a1,a2,weight=w)
                    
#COMPLETE PLOT
#nx.draw(G, with_labels=False, node_size=1, node_color="orange", width=0.2, edge_color="blue")
#plt.show()
                  
#2a
conf_int = int(input("Insert conference int:"))

# Add question "is the input id_conference or id_conference_int?" ???

if conf_int in conferences:
    authors_list=set()
    for p_int in conferences[conf_int]["pub_int"]:
        for a in publications[p_int]["authors"]:
            authors_list.add(a)
    sub_G = G.subgraph(authors_list)
    sizes = []
    for i in sub_G.nodes():
        sizes.append(15*sub_G.degree(i))

    nx.draw(sub_G, with_labels=False, node_size=sizes, node_color="orange", width=0.4, edge_color="blue")
    plt.show()


    # Centralities measures

    deg = nx.degree_centrality(sub_G)
    clos = nx.closeness_centrality(sub_G)
    bet = nx.betweenness_centrality(sub_G)

    plt.figure(1)
    plt.subplot(311)
    plt.hist(list(deg.values()))
    plt.subplot(312)
    plt.hist(list(clos.values()))
    plt.subplot(313)
    plt.hist(list(bet.values()))
    plt.show()
else:
    print("Publication not found")


# 2b
aut_id=int(input("Insert author id:"))
if aut_id in authors:
    d_value=int(input("Insert d:"))
    sub_G=nx.ego_graph(G,aut_id,radius=d_value)
    sizes=[]
    for i in sub_G:
        sizes.append(5*sub_G.degree(i))
    nx.draw(sub_G, with_labels=False, node_size=sizes, node_color="orange", width=0.4, edge_color="blue")
    plt.show()
else:
    print("Author not found")

#3   
def shortest_path_alg(source,target):
    #Step 1    
    push=hp.heappush
    pop=hp.heappop
    G_neighbors=G.adj
    reached=False
    
    temp_distances=dict([(node,float('inf')) for node in G.nodes])
    J=dict([(node,None) for node in G.nodes])
    
    final_distances={source:0}
    temp_distances[source]=0
    J[source]=0
    
    t_distances=[]
    hp.heapify(t_distances)
    
    for node,data in G_neighbors[source].items():
        push(t_distances,(data["weight"],node))
        temp_distances[node]=data["weight"]
        J[node]=source
    
    while True:
        #Step 2
        if not t_distances:
            break
        else:
            min_dist,ind=pop(t_distances)
            
            if ind in final_distances:
                continue
            
            final_distances[ind]=min_dist
            
            if ind==target:
                reached=True
                break
        
        #Step 3
        for node, data in G_neighbors[ind].items():
            if node not in final_distances:
                new_dist=final_distances[ind]+data["weight"]
                if temp_distances[node]>new_dist:
                    push(t_distances,(new_dist,node))
                    temp_distances[node]=new_dist
                    J[node]=ind
    
    if reached:
        tot=0
        path=[target]
        prev=J[target]
        while(True):
            tot+=G[prev][path[-1]]["weight"]
            path.append(prev)
            if prev==source:
                break
            else:
                prev=J[prev]     
            
        return([path[::-1],tot])
    else:
        print("PATH NOT FOUND")
        return ([[],float("inf")])
    
def multi_sorce_shortest_path_alg(sources):
    #Step 1    
    push=hp.heappush
    pop=hp.heappop
    G_neighbors=G.adj
    
    final_distances={}
    temp_distances=dict([(node,float('inf')) for node in G.nodes])
    J=dict([(node,None) for node in G.nodes])
    
    t_distances=[]
    hp.heapify(t_distances)
    
    for source in sources:
        final_distances[source]=0
        temp_distances[source]=0
        J[source]=0
        
        for node,data in G_neighbors[source].items():
            push(t_distances,(data["weight"],node))
            if temp_distances[node]>data["weight"]:
            	temp_distances[node]=data["weight"]
            	J[node]=source            	
        
    while True:
        #Step 2
        if not t_distances:
            break
        else:
            min_dist,ind=pop(t_distances)
            
            if ind in final_distances:
                continue
            
            final_distances[ind]=min_dist
        
        #Step 3
        for node, data in G_neighbors[ind].items():
            if node not in final_distances:
                new_dist=final_distances[ind]+data["weight"]
                if temp_distances[node]>new_dist:
                    push(t_distances,(new_dist,node))
                    temp_distances[node]=new_dist
                    J[node]=ind
    
    all_paths={}
    for target in G.nodes:
        if target in sources:
            all_paths[target]=[target,0]
        else:
            tot=0
            path=[target]
            prev=J[target]
            
            if prev:
                while(True):
                    tot+=G[prev][path[-1]]["weight"]
                    path.append(prev)
                    if prev in sources:
                        break
                    else:
                        prev=J[prev]
                all_paths[target]=[path[::-1],tot]
            else:
                all_paths[target]=[[],float('inf')]
                
    return(all_paths)

#3a
print("Insert author id:")                    
aut_id=int(input())

aris_id=256176


if aut_id in authors:  
    start_time = time.time()     
    
    print("Erdös Number: "+ str(shortest_path_alg(aut_id,aris_id)[1]))
       
    print("Time: %s seconds" % (time.time() - start_time))
elif aut_id==aris_id:                
    print("Source and target are the same node") 
else:
    print("Author not found")
    
#3b
print("Insert author ids (space separated):")                    
aut_ids=list(set(map(int,input().split(" "))))

if all(a in authors for a in aut_ids):
    start_time = time.time()     
    
    all_paths=multi_sorce_shortest_path_alg(aut_ids)
    
    #for k in sorted(G.nodes):
        #print("Group number ("+str(k)+") = "+str(all_paths[k][1]))
       
    for k in sorted(G.nodes)[:5]:
        print("Group number ("+str(k)+") = "+str(all_paths[k][1]))
    
    print("Time: %s seconds" % (time.time() - start_time))
else:
    print("Some authors not found")