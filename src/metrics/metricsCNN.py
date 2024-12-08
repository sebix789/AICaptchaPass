import matplotlib.pyplot as plt

def metrics_accuracy_and_loss(history,save_path_accuracy, save_path_loss):
    #Plot for Accuracy
    epochs = range(1, len(history.history['accuracy']) + 1)
    plt.figure(figsize=(12,5))
    plt.subplot(1,2,1)
    plt.plot(epochs, history.history['accuracy'], label='Accuracy on training set', color='blue')
    plt.plot(epochs, history.history['val_accuracy'], label='Accuracy on validation set', color='green')
    plt.title('Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(save_path_accuracy)
    plt.show()
    plt.close()
    #Plot for Loss
    plt.figure(figsize=(12,5))
    plt.subplot(1,2,1)
    plt.plot(epochs,history.history['loss'], label="Loss on training set", color='blue')
    plt.plot(epochs,history.history['val_loss'], label='Loss on validation set', color='green')
    plt.title('Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.grid(True)
    plt.legend()


    plt.tight_layout()
    plt.savefig(save_path_loss)
    plt.show()
    plt.close()



