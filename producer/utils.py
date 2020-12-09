import os
# import py7zr
import tarfile
import random
import sys
from glob import glob
from urllib.request import urlretrieve


EMAIL_META = [(os.environ.get('2003_EASY_HAM_2_URL'), '2003_easy_ham.tar.bz2', '2003'),
              (os.environ.get('2003_HARD_HAM_URL'),
               '2003_hard_ham.tar.bz2', '2003'),
              (os.environ.get('2003_SPAM_2_URL'), '2003_spam2.tar.bz2', '2003'),
              (os.environ.get('2005_SPAM_2_URL'), '2005_spam2.tar.bz2', '2005')]

# EMAIL_META = [ ("https://spamassassin.apache.org/old/publiccorpus/20030228_easy_ham_2.tar.bz2",
#                 '2003_easy_ham.tar.bz2', '2003'),
#                ("https://spamassassin.apache.org/old/publiccorpus/20030228_hard_ham.tar.bz2",
#                 '2003_hard_ham.tar.bz2', '2003'),
#                ("https://spamassassin.apache.org/old/publiccorpus/20030228_spam_2.tar.bz2",
#                 '2003_spam2.tar.bz2', '2003'),
#                ("https://spamassassin.apache.org/old/publiccorpus/20050311_spam_2.tar.bz2",
#                 '2005_spam2.tar.bz2', '2005')]


def download_and_extract_email_data():
    for (url, filename, _) in EMAIL_META:
        _download_file(filename=filename, url=url)

    for (_, filename, dirname) in EMAIL_META:
        _extract_bz2_data(filename=filename, dirname=dirname)


def get_n_random_email_file_names(n, email_dir_regex='*'):
    matching_email_dirs = _get_matching_email_dirs(email_dir_regex)

    matching_email_files = []
    for email_dir in matching_email_dirs:
        matching_email_files.extend(_get_email_file_names(email_dir, n))

    n = min(n, len(matching_email_files))
    sample_files = random.sample(matching_email_files, n)
    return sample_files


def _get_matching_email_dirs(email_dir_regex):
    """Pass in an email dir regex and get matching dirs

    Examples: "*ham*", "*spam*", "*easy_ham*", "*hard_ham*"
    """
    email_dirs_paths = os.path.join(
        _get_data_dir(), "*", email_dir_regex + "/")
    all_email_dirs = glob(email_dirs_paths, recursive=True)
    return all_email_dirs


def _get_email_file_names(email_dir_path, n):
    path = os.path.join(email_dir_path, "*")
    return glob(path)


def _download_file(filename, url, data_dir="./data"):
    # creates the data dir if it does not already exist
    data_dir = _get_data_dir(data_dir=data_dir)
    path_to_file = os.path.join(data_dir, filename)

    if not os.path.exists(path_to_file):
        _download_data(filename=path_to_file, url=url)


def _download_data(filename, url):
    # osFilename = os.path.join(filename)
    if not os.path.exists(filename):
        urlretrieve(url, filename)


def _extract_bz2_data(filename, dirname, data_dir='./data'):
    data_dir = _get_data_dir(data_dir=data_dir)
    path_to_file = os.path.join(data_dir, filename)

    if not os.path.exists(path_to_file):
        sys.exit("no file found! Make sure data is downloaded first!")

    path_to_target_folder = os.path.join(data_dir, dirname)
    with tarfile.open(path_to_file, "r:bz2") as tar:
        tar.extractall(path_to_target_folder)


# def _extract_7zip_data(data_dir, filename):
#     # Ensure data is available
#     if not os.path.exists(filename):
#         sys.exit("no file found! Make sure data is downloaded first!")

#     with py7zr.SevenZipFile(zip_file, mode="r") as z:
#         z.extractall(data_dir)


def _get_data_dir(data_dir=None):
    if data_dir is None:
        data_dir = os.environ.get(
            "DATA_DIR", os.path.join("/usr", "app", "data"))
    data_dir = os.path.expanduser(data_dir)
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    return data_dir
