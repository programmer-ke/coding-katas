const { createHash } = await import('node:crypto');

const hashFunction = (input_text) => {
    const hash = createHash('sha256');
    hash.update(input_text);
    return hash.digest('hex');

    let variableLengthInput = "The quick brown fox jumps over the lazy dog";
    let fixedLengthHash = hashFunction(variableLengthInput);

    console.log(fixedLengthHash);
    // outputs: d7a8fbb307d7809469ca9abcb0082e4f8d5651e46d3cdb762d02d0bf37c9e592

    console.log(fixedLengthHash.length);
    // outputs: 64
};
