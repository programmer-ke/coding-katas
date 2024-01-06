const { createHash } = await import('node:crypto');

const hashFunction = (input_text) => {
    const hash = createHash('sha256');
    hash.update(input_text);
    return hash.digest('hex');
};


let variableLengthInput = "The fox jumped over the wall";
let fixedLengthOutput = hashFunction(variableLengthInput);
console.log(fixedLengthOutput);
