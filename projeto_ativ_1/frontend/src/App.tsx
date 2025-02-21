import { useState, useEffect } from "react";
import axios from "axios";

interface Image {
  id: number;
  name: string;
  category: string;
  format: string;
  file_data: string;
}

export default function ImageManager() {
  const [images, setImages] = useState<Image[]>([]);
  const [name, setName] = useState<string>("");
  const [category, setCategory] = useState<string>("");
  const [file, setFile] = useState<File | null>(null);
  const [selectedImage, setSelectedImage] = useState<Image | null>(null);

  useEffect(() => {
    fetchImages();
  }, []);

  const fetchImages = async () => {
    const response = await axios.get<Image[]>(`/api/images/`);
    setImages(response.data);
  };

  const uploadImage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) return;
    const formData = new FormData();
    formData.append("file", file);
    formData.append("name", name);
    formData.append("category", category);
    await axios.post(`/api/upload/`, formData);
    fetchImages();
  };

  const updateImage = async (id: number) => {
    const formData = new FormData();
    if (name) formData.append("name", name);
    if (category) formData.append("category", category);
    if (file) formData.append("file", file);
    await axios.put(`/api/image/${id}`, formData);
    fetchImages();
  };

  const downloadImage = async (id: number) => {
    const response = await axios.get<{ name: string; format: string; file_data: string }>(
      `/api/download/${id}`
    );
    const link = document.createElement("a");
    link.href = `data:image/${response.data.format};base64,${response.data.file_data}`;
    link.download = response.data.name;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="p-5 bg-gray-100 min-h-screen flex flex-col items-center">
      <h1 className="text-2xl font-bold mb-4">Image Manager</h1>
      <form onSubmit={uploadImage} className="bg-white p-6 rounded-lg shadow-md mb-5 flex flex-col gap-3 w-80">
        <input className="border p-2 rounded" type="text" placeholder="Name" onChange={(e) => setName(e.target.value)} required />
        <input className="border p-2 rounded" type="text" placeholder="Category" onChange={(e) => setCategory(e.target.value)} required />
        <input className="border p-2 rounded" type="file" onChange={(e) => setFile(e.target.files ? e.target.files[0] : null)} required />
        <button className="bg-blue-500 text-white py-2 rounded hover:bg-blue-600">Upload</button>
      </form>
      <ul className="w-80">
        {images.map((img) => (
          <li key={img.id} className="bg-white p-3 rounded-lg shadow-md mb-3 flex justify-between items-center">
            <span>{img.name} - {img.category}</span>
            <div className="flex gap-2">
              <button className="bg-green-500 text-white px-2 py-1 rounded" onClick={() => setSelectedImage(img)}>View</button>
              <button className="bg-yellow-500 text-white px-2 py-1 rounded" onClick={() => updateImage(img.id)}>Update</button>
              <button className="bg-red-500 text-white px-2 py-1 rounded" onClick={() => downloadImage(img.id)}>Download</button>
            </div>
          </li>
        ))}
      </ul>
      {selectedImage && (
        <div className="mt-5 bg-white p-5 rounded-lg shadow-md text-center">
          <h2 className="text-xl font-semibold mb-2">{selectedImage.name}</h2>
          <img className="max-w-xs rounded" src={`data:image/${selectedImage.format};base64,${selectedImage.file_data}`} alt={selectedImage.name} />
        </div>
      )}
    </div>
  );
}