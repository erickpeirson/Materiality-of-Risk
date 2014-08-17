import time
import random
import londonlives
import datastorage
import dataclasses
import actions

class parseLLPage(object):
    """
    Retrieves and stores a RegistryEntry.
    """
    def __init__(self, url):
        entry = londonlives.parseItemPage(url)
        entry.id = url
        datastorage.root.londonlives[url] = entry
        datastorage.transaction.commit()
        return None

def generateParseTasks(index_url):
    urls = londonlives.listItemPages(index_url)

    for url in urls:
        task = actions.CreateDataTask(parseLLPage, url=url)
        i = len(datastorage.root.datatasks)
        datastorage.root.datatasks[i] = task
    datastorage.transaction.commit()

def executeParseTasks():
    for i,task in datastorage.root.datatasks.iteritems():
        if task.completed is None:
            task.execute()
            time.sleep(2)
    datastorage.transaction.commit()
