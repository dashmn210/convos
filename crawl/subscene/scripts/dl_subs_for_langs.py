"""
downloads a subtitle for a language

python dl_subs_for_lang.py ../data/subtitle_pages/sub_pages.txt [out_dir] [lang1] [lang2] ..
"""
from collections import defaultdict
import sys
from tqdm import tqdm
import os
import uuid
from selenium import webdriver
from ffmpy import FFmpeg
from pyunpack import Archive

sub_pages = sys.argv[1]
out_root = sys.argv[2]
langs = sys.argv[3:]
driver = webdriver.Chrome()
driver.set_page_load_timeout(10)   # 10 second limit


def download_subfile(url, dest):
    """ download a subscene file at url "url" to                                       
        the location specified by "dest"                                                 
    """
    def get_dl_button(url):
        try:
            driver.get(url)
            return driver.find_element_by_id('downloadButton')
        except Exception as e:
            print 'ERROR: cant get dl button ', url
            print e
            return False

    # download file                                                                   
    elem = get_dl_button(url)
    if not elem:
        elem = get_dl_button(url)
    if not elem:
        print 'ERROR: couldnt get dl button x2', url
        return None

    dl_link = elem.get_attribute('href')
    dl_id = str(uuid.uuid4())
    target = os.path.join(dest, dl_id)
    os.system('wget -nc -P %s %s -O %s' % (dest, dl_link, target))

    return target



def convert_all_to_srt(dir):
    """ converts all the files in a dir to srt format                                      
    """
    def convert_to_srt(target, dest):
        ff = FFmpeg(
            inputs={target: None},
            outputs={dest: None})
        ff.run()

    for f in os.listdir(dir):
        try:
            f = os.path.join(dir, f)
            if '.srt' not in f:
                convert_to_srt(f, f + '.srt')
        except:
            print 'ERROR: CONVERSION FAILURE ON', f



def extract_archive(target, dest):
    """ tries to extract an archive                                                            
    """
    try:
        Archive(target).extractall(dest)
    except:
        pass


def rm_exclude(dir, suffix):
    os.system("find %s -type f ! -name '*%s' -delete" % (dir, suffix))


def download(url, dest):
    """ downloads a file from url "url" into destination "dest",
            and then converts it to srt format
    """
    dlded_filepath = download_subfile(url, dest)
    if dlded_filepath:
        output = extract_archive(dlded_filepath, dest)
        convert_all_to_srt(dest)
        rm_exclude(dest, '.srt')
        return True
    else:
        return False





d = defaultdict(list)
urls = defaultdict(list)
for l in open(sub_pages):
    [lan, url, title] = l.strip().split()
    d[title].append(lan)
    urls[(title, lan)].append(url)

titles_to_dl = [t for t in d if all([l in d[t] for l in langs]) ]

i = 0
title_gen = ((l, t) for l in langs for t in titles_to_dl)
for l, t in tqdm(title_gen, total=len(langs)*len(titles_to_dl)):
        dl_dir = os.path.join(out_root, l, t)
        if not os.path.exists(dl_dir):
            os.makedirs(dl_dir)
        for url in urls[t, l]:
            try:
                if download(url, dl_dir):
                    pass
                else:
                    print 'failure!', url
            except KeyboardInterrupt:
                print 'QUITTING'
                quit()
            except Exception as e:
                print 'ERROR on ', url, 'exception ', e
        i += 1

