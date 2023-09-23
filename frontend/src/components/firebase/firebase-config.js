// Import the functions you need from the SDKs you need
import { initializeApp }    from "firebase/app";
import { getStorage } from "firebase/storage";

// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyDci14vP0nqfyDyDymcFTG0CgZyAJLhPvg",
  authDomain: "cancertumorbootcampdosboots.firebaseapp.com",
  projectId: "cancertumorbootcampdosboots",
  storageBucket: "cancertumorbootcampdosboots.appspot.com",
  messagingSenderId: "1025730251750",
  appId: "1:1025730251750:web:bfcd620d8dcfa2ad502427",
  measurementId: "G-HTJRM0LT10"
};

// Initialize Firebase
const app      = initializeApp(firebaseConfig);
const DataBase = getStorage(app);

export default DataBase;