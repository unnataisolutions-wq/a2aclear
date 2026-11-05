import * as crypto from 'crypto';
import { TaskContract, ContractState } from './contract';
import { AgentIdentity } from './identity';

export interface EscrowRecord {
  escrowId: string;
  taskId: string;
  originatorDid: string;
  providerDid: string;
  totalAmountPaise: number;
  providerPayoutPaise: number;
  protocolFeePaise: number;
  status: 'LOCKED' | 'SETTLED' | 'REFUNDED';
  lockedAt: number;
  expiresAt: number;
  expectedArtifactHash: string;
  deliverableHash?: string;
  settledAt?: number;
}

export interface SettlementReceipt {
  receiptType: string;
  taskId: string;
  escrowId: string;
  originatorDid: string;
  providerDid: string;
  grossAmountPaise: number;
  providerReceivedPaise: number;
  protocolFeePaise: number;
  deliverableHash: string;
  settledAt: number;
  settlementHash: string;
  clearinghouseSignature?: string;
  clearinghouseDid?: string;
}

export class MicroEscrowVault {
  public treasuryDid: string;
  public balances: Map<string, number> = new Map();
  public escrows: Map<string, EscrowRecord> = new Map();

  constructor(treasuryDid: string = 'did:a2a:treasury_unnat_master') {
    this.treasuryDid = treasuryDid;
  }

  public deposit(did: string, amountPaise: number): void {
    if (amountPaise <= 0) throw new Error('Deposit amount must be positive.');
    const current = this.balances.get(did) || 0;
    this.balances.set(did, current + amountPaise);
  }

  public getBalance(did: string): number {
    return this.balances.get(did) || 0;
  }

  public lockEscrow(contract: TaskContract): EscrowRecord {
    const balance = this.getBalance(contract.originatorDid);
    if (balance < contract.amountPaise) {
      throw new Error(`Insufficient vault funds. Balance: ${balance}, Required: ${contract.amountPaise}`);
    }

    this.balances.set(contract.originatorDid, balance - contract.amountPaise);
    const escrowId = `escrow_${crypto.randomBytes(8).toString('hex')}`;

    const record: EscrowRecord = {
      escrowId,
      taskId: contract.taskId,
      originatorDid: contract.originatorDid,
      providerDid: contract.providerDid,
      totalAmountPaise: contract.amountPaise,
      providerPayoutPaise: contract.providerPayoutPaise,
      protocolFeePaise: contract.protocolFeePaise,
      status: 'LOCKED',
      lockedAt: Math.floor(Date.now() / 1000),
      expiresAt: Math.floor(Date.now() / 1000) + contract.slaTimeoutSeconds,
      expectedArtifactHash: contract.taskSpecHash,
    };

    this.escrows.set(contract.taskId, record);
    contract.state = ContractState.ESCROW_LOCKED;
    return record;
  }

  public verifyAndSettle(
    contract: TaskContract,
    deliverable: any,
    clearinghouseIdentity?: AgentIdentity
  ): SettlementReceipt {
    const escrow = this.escrows.get(contract.taskId);
    if (!escrow || escrow.status !== 'LOCKED') {
      throw new Error(`Escrow not found or not in LOCKED state for task ${contract.taskId}`);
    }

    const deliverableBytes = typeof deliverable === 'string'
      ? Buffer.from(deliverable, 'utf-8')
      : Buffer.from(JSON.stringify(deliverable), 'utf-8');
    const computedHash = crypto.createHash('sha256').update(deliverableBytes).digest('hex');

    const providerBalance = this.getBalance(contract.providerDid);
    const treasuryBalance = this.getBalance(this.treasuryDid);

    this.balances.set(contract.providerDid, providerBalance + escrow.providerPayoutPaise);
    this.balances.set(this.treasuryDid, treasuryBalance + escrow.protocolFeePaise);

    escrow.status = 'SETTLED';
    escrow.settledAt = Math.floor(Date.now() / 1000);
    escrow.deliverableHash = computedHash;
    contract.state = ContractState.SETTLED;

    const receiptData = {
      receiptType: 'A2ACLEAR_SETTLEMENT_RECEIPT_V1',
      taskId: contract.taskId,
      escrowId: escrow.escrowId,
      originatorDid: contract.originatorDid,
      providerDid: contract.providerDid,
      grossAmountPaise: escrow.totalAmountPaise,
      providerReceivedPaise: escrow.providerPayoutPaise,
      protocolFeePaise: escrow.protocolFeePaise,
      deliverableHash: computedHash,
      settledAt: escrow.settledAt,
    };

    const canonicalReceipt = JSON.stringify(receiptData, Object.keys(receiptData).sort());
    const settlementHash = crypto.createHash('sha256').update(canonicalReceipt).digest('hex');
    contract.settlementHash = settlementHash;

    const receipt: SettlementReceipt = {
      ...receiptData,
      settlementHash,
    };

    if (clearinghouseIdentity) {
      receipt.clearinghouseSignature = clearinghouseIdentity.sign(settlementHash);
      receipt.clearinghouseDid = clearinghouseIdentity.did;
    }

    return receipt;
  }
}
