const { onObjectFinalized } = require("firebase-functions/v2/storage");
const { initializeApp } = require("firebase-admin/app");
const { getStorage } = require("firebase-admin/storage");
const { getFirestore, FieldValue } = require("firebase-admin/firestore");

const path = require("path");
const os = require("os");
const fs = require("fs");
const pdfParse = require("pdf-parse");

initializeApp();

exports.extractResumeText = onObjectFinalized(async (event) => {
  const file = event.data;
  if (!file || !file.name || !file.bucket) {
    console.error("Missing file data in event.");
    return;
  }

  const filePath = file.name;
  const fileName = path.basename(filePath);
  const bucket = getStorage().bucket(file.bucket);

  if (!filePath.endsWith(".pdf")) {
    console.log("Not a PDF file. Skipping...");
    return;
  }

  const tempFilePath = path.join(os.tmpdir(), fileName);
  await bucket.file(filePath).download({ destination: tempFilePath });

  const dataBuffer = fs.readFileSync(tempFilePath);
  const data = await pdfParse(dataBuffer);
  const extractedText = data.text;

  const parts = filePath.split("/");
  const userId = parts[1];

  const resumesSnapshot = await getFirestore()
            .collection("hireinn_users")
            .doc(userId)
            .collection("resumes")
            .where("storagePath", "==", filePath)
            .limit(1)
            .get();

            if (!resumesSnapshot.empty) {
                const resumeDoc = resumesSnapshot.docs[0];
                await resumeDoc.ref.update({
                    resumeText: extractedText,
                    processingStatus: "completed",
                    processedAt: FieldValue.serverTimestamp(),
                });
                console.log("Resume text updated in Firestore.");
            }
  console.log("fileName: " + fileName);
  console.log("storageUrl: " + filePath);
  console.log("Bucket: " + file.bucket);
  console.log("Resume text length: " + extractedText.length);
  console.log("Resume text extracted and stored.");
});
