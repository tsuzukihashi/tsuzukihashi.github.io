// QR を Apple の Vision（iPhone のカメラと同じ読み取り）で読む。 swiftc -O -o /tmp/qr_vision docs/meishi/qr_vision.swift && /tmp/qr_vision <png...>
import Vision
import AppKit
for p in CommandLine.arguments.dropFirst() {
    guard let img = NSImage(contentsOfFile: p) else { print(p, "読めない"); continue }
    var r = CGRect(origin: .zero, size: img.size)
    let cg = img.cgImage(forProposedRect: &r, context: nil, hints: nil)!
    let req = VNDetectBarcodesRequest()
    req.symbologies = [.qr]
    try? VNImageRequestHandler(cgImage: cg).perform([req])
    let got = (req.results ?? []).compactMap { $0.payloadStringValue }
    print((p as NSString).lastPathComponent, got.isEmpty ? "×読めない" : got.joined(separator: ","))
}
