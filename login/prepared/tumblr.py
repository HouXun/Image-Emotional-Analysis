import pytumblr
import os
import csv
import io
import pandas as pd
import tensorflow as tf

from PIL import Image
from urllib.request import urlopen
class tumblr():
    def extract_tumblr_posts(client, nb_requests, search_query, before, delta_limit):
        posts = []
        for i in range(nb_requests):
            print('i:', i, 'tag:', search_query)
            tagged = client.tagged(search_query, filter='text', before=before)
            for elt in tagged:
                try:
                    timestamp = elt['timestamp']
                    print('difference:', abs(timestamp - before))
                    if (abs(timestamp - before) < delta_limit):
                        before = timestamp
                        current_post = []
                        current_post.append(elt['id'])
                        current_post.append(elt['post_url'])
                        elt_type = elt['type']
                        current_post.append(elt_type)
                        current_post.append(timestamp)
                        current_post.append(elt['date'])
                        current_post.append(elt['tags'])
                        current_post.append(elt['liked'])
                        current_post.append(elt['note_count'])

                        if (elt_type == 'photo'):
                            # Only take the first image
                            current_post.append(elt['photos'][0]['original_size']['url'])
                            current_post.append(elt['caption'].replace('\n', ' ').replace('\r', ' '))
                            current_post.append(search_query)
                            posts.append(current_post)

                except TypeError:
                    print("Error")
                    continue
        return posts

    def save_csv(self,csv_dir):
        client = pytumblr.TumblrRestClient(
            'dSzyxGsJ72cXUkoobt1TVug8wag6AzVCKlbrccBhWb2kbavKCO',
            '10JMaTu2eglGJCzEpeQI6Vt4gcVySRvdyVUBk0iVLqbkVALc0v',
            '5bTiJMhYd7UPN0fEXNgNvtR4xvco8JmV5TCtvFZjTpOGIeNgAd',
            'CLKCx31ljxzIw5QZqsszvd1tjjGOvLLwBYXjJ5CXEQzmyMGS6s'
        )

        # Make the request
        print(client.info())

        before = 1500000000
        delta_limit = 10000000

        tags = ['Happy', 'Calm', 'Sad', 'Scared', 'Bored', 'Angry', 'Annoyed', 'Love', 'Excited', 'Surprised',
                'Optimistic', 'Amazed', 'Ashamed', 'Disgusted', 'Pensive']
        title = ['id', 'post_url', 'type', 'timestamp', 'date', 'tags', 'liked', 'note_count', 'photo', 'caption',
                 'search_query']

        for tag in tags:
            posts = self.extract_tumblr_posts(client, 500, tag, before, delta_limit)
            print('length', len(posts))
            csv_path = os.path.join(csv_dir, tag + '.csv')
            csvFile = open(csv_path, 'w', newline='', encoding='utf-8')  # 设置newline，否则两行之间会空一行
            writer = csv.writer(csvFile)
            writer.writerow(title)
            for post in posts:
                writer.writerow(post)
            csvFile.close()

    def download_im(search_query, start, end, dataset_dir, subdir='photos'):
        # Load data
        df = pd.read_csv(os.path.join(dataset_dir, search_query + '.csv'), encoding='utf-8')
        links = df['photo']
        # Create subdir if it doesn't exist
        if not tf.gfile.Exists(os.path.join(dataset_dir, subdir)):
            tf.gfile.MakeDirs(os.path.join(dataset_dir, subdir))
        # Create search_query folder if it doesn't exist
        photos_dir = os.path.join(dataset_dir, subdir, search_query)
        if not tf.gfile.Exists(photos_dir):
            tf.gfile.MakeDirs(photos_dir)
        # for i in range(start, end):
        for i in range(len(links)):
            # Check for NaNs
            if links[i] == links[i]:
                print(links[i])
                # Open url and convert to JPEG image
                if links[i][-3:] == 'gif':
                    if i >= 1 and links[i - 1][-3:] == 'gif':
                        continue
                try:
                    f = urlopen(links[i], timeout=60)
                except Exception:
                    print('Exception')
                    continue

                image_file = io.BytesIO(f.read())
                im = Image.open(image_file)
                # The filename is the index of the image in the dataframe
                filename = str(i) + '.jpeg'
                im.convert('RGB').save(os.path.join(photos_dir, filename), 'JPEG')
