#Clustering with Kruskal's Algorithm
#mehmetalikomurcu

import tkinter as tk
import random
import math
import statistics
import Node
import Edge

def euclidean_distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

def Find(i, nodes):
    if i != nodes[i].parent:
        nodes[i].parent = Find(nodes[i].parent, nodes)
    return nodes[i].parent

def Union(u, v, nodes):
    r1 = Find(u, nodes)
    r2 = Find(v, nodes)
    if r1 != r2:
        if nodes[r1].rank > nodes[r2].rank:
            nodes[r2].parent = r1
        else:
            nodes[r1].parent = r2
            if nodes[r1].rank == nodes[r2].rank:
                nodes[r2].rank += 1

def clustering(x, y, k):
    n = len(x)
    edges = []
    nodes = []

    for i in range(n):
        nodes.append(Node.Node(x[i], y[i], i))

    for i in range(n):
        for j in range(i + 1, n):
            edges.append(Edge.Edge(i, j, euclidean_distance(x[i], y[i], x[j], y[j])))

    edges = sorted(edges, key=lambda edge: edge.weight)

    num_edges_added = 0
    for edge in edges:
        if Find(edge.u, nodes) != Find(edge.v, nodes):
            num_edges_added += 1
            Union(edge.u, edge.v, nodes)
        if num_edges_added > n - k-1:
            break

    clusters = [-1] * n
    cluster_index = 0
    for i in range(n):
        if clusters[i] == -1:
            clusters[i] = cluster_index
            cluster_index += 1
            for j in range(i + 1, n):
                if Find(i, nodes) == Find(j, nodes):
                    clusters[j] = clusters[i]

    return clusters

def visualize_clustering(canvas, x, y, clusters, centers):
    for star in star_texts:
        canvas.delete(star)

    colors = ['red', 'green', 'blue', 'cyan', 'magenta', 'yellow', 'black',
              'orange', 'purple', 'brown', 'pink', 'teal', 'maroon', 'navy',
              'olive', 'lime', 'aqua', 'fuchsia', 'silver', 'gray']
    counter = 0

    for i in range(len(x)):
        cluster_index = clusters[i]
        canvas.create_oval(x[i] - 5, y[i] - 5, x[i] + 5, y[i] + 5, fill=colors[cluster_index])

    for center in centers:
        star_texts.append(canvas.create_text(center[0], center[1], text='*', font=('Arial', 36), fill=colors[counter]))
        counter+=1


def add_points_button_callback(canvas, x, y, n):
    new_x_points = [random.randint(10, 490) for _ in range(n)]
    new_y_points = [random.randint(10, 490) for _ in range(n)]
    x.extend(new_x_points)
    y.extend(new_y_points)
    visualize_points(canvas, x, y)

def add_points_click_callback(event, canvas, x, y):
    new_x_points = [event.x]
    new_y_points = [event.y]
    x.extend(new_x_points)
    y.extend(new_y_points)
    visualize_points(canvas, x, y)

def cluster_button_callback(canvas, x, y, k):
    clusters = clustering(x, y, k)
    center_points = []
    for i in range(k):
        cluster_x = [x_points[j] for j in range(len(x_points)) if clusters[j] == i]
        cluster_y = [y_points[j] for j in range(len(y_points)) if clusters[j] == i]

        if cluster_x and cluster_y:
            center_x = sum(cluster_x) / len(cluster_x)
            center_y = sum(cluster_y) / len(cluster_y)
            center_points.append((center_x, center_y))
        else:
            # Küme boşsa veya hiç eleman yoksa, rastgele bir merkez belirlenebilir veya uygun bir değer atanabilir.
            # Bu örnekte, (0, 0) noktasını kullanıyoruz.
            center_points.append((0, 0))

    visualize_clustering(canvas, x_points, y_points, clusters, center_points)
    display_statistics(root, x_points, y_points, clusters, center_points, stat_labels)

def visualize_points(canvas, x, y):
    canvas.delete("all")
    for i in range(len(x)):
        canvas.create_oval(x[i] - 5, y[i] - 5, x[i] + 5, y[i] + 5, fill='black')

def display_statistics(root, x, y, clusters, centers, stat_labels):
    for label in stat_labels:
        label.destroy()

    total_points = len(x)
    cluster_sizes = [clusters.count(i) for i in set(clusters)]

    stats_label = tk.Label(root, text="İstatistik Bilgileri", font=('Arial', 12, 'bold'))
    stats_label.pack()
    stat_labels.append(stats_label)

    total_label = tk.Label(root, text=f"Toplam Nokta Sayısı: {total_points}")
    total_label.pack()
    stat_labels.append(total_label)

    for i, size in enumerate(cluster_sizes):
        cluster_label = tk.Label(root, text=f"\nKüme {i+1} Nokta Sayısı: {size}")
        cluster_label.pack()
        stat_labels.append(cluster_label)

        cluster_x = [x[j] for j in range(total_points) if clusters[j] == i]
        cluster_y = [y[j] for j in range(total_points) if clusters[j] == i]

        if size > 1:
            std_dev = statistics.stdev(cluster_x + cluster_y)
            variance = statistics.variance(cluster_x + cluster_y)
        else:
            std_dev = 0
            variance = 0

        std_dev_label = tk.Label(root, text=f"Küme {i+1} Standart Sapma: {std_dev:.2f}")
        std_dev_label.pack()
        stat_labels.append(std_dev_label)

        variance_label = tk.Label(root, text=f"Küme {i+1} Varyans: {variance:.2f}")
        variance_label.pack()
        stat_labels.append(variance_label)

    center_label = tk.Label(root, text=f"\nKüme Merkezi Noktaları: {centers}")
    center_label.pack()
    stat_labels.append(center_label)


if __name__ == '__main__':

    x_points = []
    y_points = []
    stat_labels = [] 
    star_texts = [] 
    root = tk.Tk()
    root.title("Kruskal Algoritması ile Kümeleme Uygulaması")

    frame = tk.Frame(root)
    frame.pack()


    frame = tk.Frame(root)
    frame.pack(side="left", padx=10, pady=10)

    canvas = tk.Canvas(frame, width=500, height=500, bg="white")
    canvas.pack(side="right", padx=5)
    
    num_points_entry = tk.Entry(frame, width=5, font=("Helvetica", 12))
    num_points_entry.pack(pady=(100,20))
    num_points_entry.insert(0, "5")  # Varsayılan olarak 5 nokta

    random_points_button = tk.Button(frame,width=20,font=("Helvetica", 12), text="Rastgele Nokta Ekle", command=lambda : add_points_button_callback(canvas,x_points, y_points,int(num_points_entry.get())))
    random_points_button.pack(padx=5)

    cluster_entry = tk.Entry(frame, width=5, font=("Helvetica", 12))
    cluster_entry.pack(pady=(100,20))
    cluster_entry.insert(0, "3")  # Varsayılan olarak 3 küme

    cluster_button = tk.Button(frame,width=20,font=("Helvetica", 12), text="Kümeleme", command=lambda: cluster_button_callback(canvas, x_points, y_points, int(cluster_entry.get())))
    cluster_button.pack( padx=5, pady=(0,20))

    canvas.bind("<Button-1>", lambda event: add_points_click_callback(event, canvas, x_points, y_points))
    
    root.mainloop()
