from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
import pandas as pd

app = Flask(__name__)

class ImageYielder:
    def __init__(self):
        df = pd.read_csv('../mech_turk_youtube.csv')
        self.image_urls = list(df['image_url'].sample(frac=1)) # randomize dataframe
        self.seen_urls = set()

    def get_random_image_url_without_replacement(self):
        for path in self.image_urls:
            yield path

    def get_next_image(self):
        for image in self.get_random_image_url_without_replacement():
            if image not in self.seen_urls:
                return image

iy = ImageYielder()

@app.route('/image-labeling-youtube', methods=['GET'])
def label_images():
    """ Displays different images on refresh
    """
    content = {}
    content['image_url'] = iy.get_next_image()
    return render_template('mturk.html', **content)


@app.route('/submit-results', methods=['POST'])
def save_results():
    image_url = request.form['image_url']
    image_text = request.form['image_text']
    if (image_text == ""):
        return redirect('/image-labeling-youtube')
    iy.seen_urls.add(image_url)
    with open('youtube-titles.csv', 'a') as out:
        print(f"{image_url},{image_text}", sep='\n', file=out)
    return redirect('/image-labeling-youtube')



if __name__ == '__main__':
    app.run(debug=True)
