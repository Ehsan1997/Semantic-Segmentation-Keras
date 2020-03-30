import matplotlib.pyplot as plt
%matplotlib inline
plt.rcParams['figure.figsize'] = (10.0, 8.0) # set default size of plots
plt.rcParams['image.interpolation'] = 'nearest'
plt.rcParams['image.cmap'] = 'gray'

def load(image_path): #Load an image from a file path
    return cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2RGB)

def display(image, title=None): # Show image
    plt.figure(figsize = (5,5))
    plt.imshow(image)
    plt.axis('off')
    if title: plt.title(title)
    plt.show()

def display_masked(image, mask): # Show image with its segmentation mask
    masked_image = image.copy()
    mask_resized = image.copy()

    mask_resized[:,:,0] = mask[:,:,0]
    mask_resized[:,:,1] = mask[:,:,0]
    mask_resized[:,:,2] = mask[:,:,0]

    plt.figure(figsize = (20,20))
    plt.subplot(1,3,1)
    plt.imshow(image, 'gray')
    plt.title("Tissue Image")
    plt.axis('off')
    plt.subplot(1,3,2)
    plt.imshow(mask_resized, 'gray')
    plt.title("Ground Truth")
    plt.axis('off')
    plt.subplot(1,3,3)
    plt.imshow(masked_image, 'gray')
    plt.imshow(mask_resized, 'jet', alpha=0.5)
    plt.title("Tissue Image with Ground Truth overlapped")
    plt.axis('off')
    plt.show()
