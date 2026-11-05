import * as crypto from 'crypto';

export enum ContractState {
  PROPOSED = 'PROPOSED',
  NEGOTIATING = 'NEGOTIATING',
  AGREED = 'AGREED',
  ESCROW_LOCKED = 'ESCROW_LOCKED',
  SETTLED = 'SETTLED',
  DISPUTED = 'DISPUTED',
  SLASHED = 'SLASHED',
}

export const PROTOCOL_INTERCHANGE_BPS = 50; // 0.50%

export interface TaskContractConfig {
  taskId: string;
  originatorDid: string;
  providerDid: string;
  amountPaise: number;
  currency?: string;
  slaTimeoutSeconds?: number;
  taskSpecHash?: string;
}

export class TaskContract {
  public taskId: string;
  public originatorDid: string;
  public providerDid: string;
  public amountPaise: number;
  public currency: string;
  public slaTimeoutSeconds: number;
  public taskSpecHash: string;
  public createdAt: number;
  public state: ContractState;

  public protocolFeePaise: number;
  public providerPayoutPaise: number;

  public originatorSignature?: string;
  public providerSignature?: string;
  public settlementHash?: string;

  constructor(config: TaskContractConfig) {
    this.taskId = config.taskId;
    this.originatorDid = config.originatorDid;
    this.providerDid = config.providerDid;
    this.amountPaise = config.amountPaise;
    this.currency = config.currency || 'INR';
    this.slaTimeoutSeconds = config.slaTimeoutSeconds || 300;
    this.taskSpecHash = config.taskSpecHash || '';
    this.createdAt = Math.floor(Date.now() / 1000);
    this.state = ContractState.PROPOSED;

    this.protocolFeePaise = Math.floor((this.amountPaise * PROTOCOL_INTERCHANGE_BPS) / 10000);
    this.providerPayoutPaise = this.amountPaise - this.protocolFeePaise;
  }

  public computeContractHash(): string {
    const data = {
      taskId: this.taskId,
      originatorDid: this.originatorDid,
      providerDid: this.providerDid,
      amountPaise: this.amountPaise,
      currency: this.currency,
      taskSpecHash: this.taskSpecHash,
      createdAt: this.createdAt,
    };
    const canonical = JSON.stringify(data, Object.keys(data).sort());
    return crypto.createHash('sha256').update(canonical, 'utf-8').digest('hex');
  }

  public toJSON() {
    return {
      taskId: this.taskId,
      originatorDid: this.originatorDid,
      providerDid: this.providerDid,
      amountPaise: this.amountPaise,
      currency: this.currency,
      protocolFeePaise: this.protocolFeePaise,
      providerPayoutPaise: this.providerPayoutPaise,
      slaTimeoutSeconds: this.slaTimeoutSeconds,
      taskSpecHash: this.taskSpecHash,
      createdAt: this.createdAt,
      state: this.state,
      originatorSignature: this.originatorSignature,
      providerSignature: this.providerSignature,
      settlementHash: this.settlementHash,
    };
  }
}
