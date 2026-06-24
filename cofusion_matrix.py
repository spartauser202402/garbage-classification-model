#from sklearn.metrics import confusion_matrix
#import seaborn as sns
#import numpy as np

#y_true = []
#y_pred = []

#for images, labels in val_ds:
#   preds = model.predict(images, verbose=0)

#    y_true.extend(labels.numpy())
#    y_pred.extend(np.argmax(preds, axis=1))

#cm = confusion_matrix(y_true, y_pred)

#plt.figure(figsize=(6,5))
#sns.heatmap(
#    cm,
#    annot=True,
#    fmt='d',
#    xticklabels=class_names,
#    yticklabels=class_names
#)

#plt.xlabel("Predicted")
#plt.ylabel("Actual")
#plt.show()
