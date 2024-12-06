import winzy
import urllib.parse
import webbrowser
import sys
import os
import tempfile
import requests

def generate_url(text):
    return f"https://maxm-imggenurl.web.val.run/{urllib.parse.quote(text)}"

def get_text_from_input(args):
    if len(args.text) == 0:
        text = sys.stdin.read()
    else:
        text = " ".join(args.text)
    return text.strip()

def handle_high_resolution(text, args):
    hdtext = "high resolution, high quality photo, 8k canon camera"
    if args.hd:
        text += hdtext
    return text

def truncate_text(text):
    max_length = 300
    if len(text) > max_length:
        print(f"Warning: Text is too long. Truncating to {max_length} characters.")
    return text[:max_length]

def save_image(url, temp_dir):
    response = requests.get(url)
    if response.status_code == 200:
        filename = os.path.join(temp_dir, f"image_{os.urandom(4).hex()}.png")
        with open(filename, 'wb') as file:
            file.write(response.content)
        print(f"Image saved to {filename}")
    else:
        print(f"Failed to download image. Status code: {response.status_code}")



def create_parser(subparser):
    parser = subparser.add_parser("t2i", description="Text to Image Gen Using Val Town's imggenurl ")
    # Add subprser arguments here.
    parser.add_argument("text", nargs="*", help="Text to generate URL for")
    parser.add_argument("-hd", action="store_true", help="If provided, add prompt to generate high resolution")
    parser.add_argument("-s", "--save", action="store_true", help="Save the generated image to a temporary file instead of opening in web browser")

    return parser


class HelloWorld:
    """ An text to image using val town imggenurl plugin """
    __name__ = "t2i"

    @winzy.hookimpl
    def register_commands(self, subparser):
        parser = create_parser(subparser)
        parser.set_defaults(func=self.main)

    def main(self, args):
        text = get_text_from_input(args)
        text = handle_high_resolution(text, args)
        text = truncate_text(text)

        url = generate_url(text)

        if args.save:
            temp_dir = tempfile.mkdtemp()
            save_image(url, temp_dir)
        else:
            print(f"Opening URL: {url}")
            webbrowser.open(url, 1)
    
    def hello(self, args):
        # this routine will be called when "winzy t2i is called."
        print("Hello! This is an example ``winzy`` plugin.")

t2i_plugin = HelloWorld()
