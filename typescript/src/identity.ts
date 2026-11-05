import * as crypto from 'crypto';

export interface A2AEnvelope<T = any> {
  a2a_version: string;
  sender_did: string;
  recipient_did: string;
  timestamp: number;
  nonce: number;
  action: string;
  payload: T;
  signature?: string;
}

export class AgentIdentity {
  public readonly publicKeyPem: string;
  public readonly privateKeyPem: string;
  public readonly pubkeyHex: string;
  public readonly did: string;

  private privateKeyObj: crypto.KeyObject;
  private publicKeyObj: crypto.KeyObject;

  constructor(privateKeyPem?: string) {
    if (!privateKeyPem) {
      const { publicKey, privateKey } = crypto.generateKeyPairSync('ed25519');
      this.privateKeyObj = privateKey;
      this.publicKeyObj = publicKey;
      this.privateKeyPem = privateKey.export({ type: 'pkcs8', format: 'pem' }) as string;
      this.publicKeyPem = publicKey.export({ type: 'spki', format: 'pem' }) as string;
    } else {
      this.privateKeyPem = privateKeyPem;
      this.privateKeyObj = crypto.createPrivateKey(privateKeyPem);
      this.publicKeyObj = crypto.createPublicKey(this.privateKeyObj);
      this.publicKeyPem = this.publicKeyObj.export({ type: 'spki', format: 'pem' }) as string;
    }

    const rawPub = this.publicKeyObj.export({ type: 'spki', format: 'der' });
    // In SPKI Ed25519, the last 32 bytes are the raw public key
    const raw32 = rawPub.subarray(rawPub.length - 32);
    this.pubkeyHex = raw32.toString('hex');
    this.did = `did:a2a:${this.pubkeyHex}`;
  }

  public static generate(): AgentIdentity {
    return new AgentIdentity();
  }

  public sign(data: Buffer | string): string {
    const buf = typeof data === 'string' ? Buffer.from(data, 'utf-8') : data;
    return crypto.sign(null, buf, this.privateKeyObj).toString('hex');
  }

  public signEnvelope<T = any>(payload: T, action: string, recipientDid: string = '*'): A2AEnvelope<T> {
    const envelope: A2AEnvelope<T> = {
      a2a_version: '1.0.0',
      sender_did: this.did,
      recipient_did: recipientDid,
      timestamp: Math.floor(Date.now() / 1000),
      nonce: Math.floor(Math.random() * 1000000000),
      action,
      payload,
    };

    const canonicalStr = JSON.stringify(envelope, Object.keys(envelope).sort());
    envelope.signature = this.sign(canonicalStr);
    return envelope;
  }

  public static verifyEnvelope(envelope: A2AEnvelope): boolean {
    try {
      if (!envelope.signature || !envelope.sender_did.startsWith('did:a2a:')) {
        return false;
      }
      const pubkeyHex = envelope.sender_did.replace('did:a2a:', '').trim();
      const rawPub = Buffer.from(pubkeyHex, 'hex');

      // Reconstruct SPKI for Node crypto Ed25519
      // Ed25519 SPKI prefix: 302a300506032b6570032100
      const spkiPrefix = Buffer.from('302a300506032b6570032100', 'hex');
      const spkiDer = Buffer.concat([spkiPrefix, rawPub]);
      const publicKey = crypto.createPublicKey({ key: spkiDer, format: 'der', type: 'spki' });

      const envCopy = { ...envelope };
      delete envCopy.signature;
      const canonicalStr = JSON.stringify(envCopy, Object.keys(envCopy).sort());

      return crypto.verify(null, Buffer.from(canonicalStr, 'utf-8'), publicKey, Buffer.from(envelope.signature, 'hex'));
    } catch {
      return false;
    }
  }
}
