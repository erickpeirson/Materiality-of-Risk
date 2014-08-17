import ZODB, ZODB.FileStorage, BTrees.IOBTree, BTrees.OOBTree, transaction

datapath = './data/datastore.fs'

storage = ZODB.FileStorage.FileStorage(datapath)
db = ZODB.DB(storage)
connection = db.open()
root = connection.root

if not hasattr(root, 'datatasks'):
    root.datatasks = BTrees.IOBTree.BTree()
    transaction.commit()

if not hasattr(root, 'londonlives'):
    root.londonlives = BTrees.OOBTree.BTree()
    transaction.commit()